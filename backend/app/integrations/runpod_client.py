"""
RunPod API Client for Iyke Content Studio.

Handles GPU pod lifecycle, serverless job submission, network volume
management, and health monitoring through the RunPod REST API v2.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

RUNPOD_API_BASE = "https://api.runpod.io/v2"
RUNPOD_SERVERLESS_BASE = "https://api.runpod.ai/v2"


@dataclass
class Pod:
    """Represents a RunPod GPU pod instance."""
    id: str = ""
    name: str = ""
    gpu_type: str = ""
    gpu_count: int = 1
    status: str = ""
    desired_status: str = ""
    cost_per_hour: float = 0.0
    image_name: str = ""
    volume_id: Optional[str] = None
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class PodStatus:
    """Status of a RunPod pod."""
    id: str = ""
    status: str = ""
    desired_status: str = ""
    cost_per_hour: float = 0.0
    runtime_seconds: int = 0


@dataclass
class Volume:
    """RunPod network volume."""
    id: str = ""
    name: str = ""
    size_gb: int = 0
    datacenter_id: str = ""


@dataclass
class GpuType:
    """Available GPU type on RunPod."""
    id: str = ""
    display_name: str = ""
    memory_gb: int = 0
    secure_cloud_price: float = 0.0
    community_cloud_price: float = 0.0


@dataclass
class JobStatus:
    """Status of a serverless job."""
    id: str = ""
    status: str = ""  # IN_QUEUE, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int = 0


class RunPodClient:
    """
    Client for interacting with the RunPod API.

    Supports:
    - Pod management (create, start, stop, terminate)
    - Serverless job submission and monitoring
    - Network volume management
    - GPU type discovery
    - Health checks
    """

    def __init__(self, api_key: str, timeout: float = 30.0):
        """Initialize the RunPod client.

        Args:
            api_key: RunPod API key for authentication.
            timeout: Default request timeout in seconds.
        """
        self.api_key = api_key
        self.timeout = timeout
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _client(self) -> httpx.AsyncClient:
        """Create a new async HTTP client with auth headers."""
        return httpx.AsyncClient(
            headers=self._headers,
            timeout=self.timeout,
        )

    # ── Pod Management ──

    async def create_pod(
        self,
        name: str,
        image: str,
        gpu_type: str,
        volume_id: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        container_disk_gb: int = 50,
        volume_disk_gb: int = 100,
        ports: str = "8888/HTTP,22/TCP",
    ) -> Pod:
        """Create and start a new GPU pod.

        Args:
            name: Display name for the pod.
            image: Docker image to run.
            gpu_type: GPU type ID (e.g., 'NVIDIA GeForce RTX 4090').
            volume_id: Optional network volume ID to attach.
            env: Environment variables for the container.
            container_disk_gb: Size of ephemeral container disk.
            volume_disk_gb: Size of persistent volume disk.
            ports: Comma-separated port mappings.

        Returns:
            Pod object with creation details.
        """
        payload: dict[str, Any] = {
            "name": name,
            "imageName": image,
            "gpuTypeId": gpu_type,
            "gpuCount": 1,
            "containerDiskInGb": container_disk_gb,
            "volumeDiskInGb": volume_disk_gb,
            "ports": ports,
        }

        if volume_id:
            payload["networkVolumeId"] = volume_id

        if env:
            payload["env"] = [{"key": k, "value": v} for k, v in env.items()]

        async with self._client() as client:
            response = await client.post(f"{RUNPOD_API_BASE}/pods", json=payload)
            response.raise_for_status()
            data = response.json()

        logger.info(f"Created pod {data.get('id')} with GPU {gpu_type}")
        return Pod(
            id=data.get("id", ""),
            name=name,
            gpu_type=gpu_type,
            status=data.get("desiredStatus", "RUNNING"),
            desired_status=data.get("desiredStatus", "RUNNING"),
            cost_per_hour=data.get("costPerHr", 0.0),
            image_name=image,
            volume_id=volume_id,
            env=env or {},
        )

    async def start_pod(self, pod_id: str) -> PodStatus:
        """Start/resume a stopped pod."""
        async with self._client() as client:
            response = await client.post(f"{RUNPOD_API_BASE}/pods/{pod_id}/start")
            response.raise_for_status()
            data = response.json()

        logger.info(f"Started pod {pod_id}")
        return PodStatus(id=pod_id, status="RUNNING", desired_status="RUNNING")

    async def stop_pod(self, pod_id: str) -> PodStatus:
        """Stop a running pod (releases GPU, keeps volume)."""
        async with self._client() as client:
            response = await client.post(f"{RUNPOD_API_BASE}/pods/{pod_id}/stop")
            response.raise_for_status()

        logger.info(f"Stopped pod {pod_id}")
        return PodStatus(id=pod_id, status="EXITED", desired_status="EXITED")

    async def terminate_pod(self, pod_id: str) -> bool:
        """Terminate and destroy a pod completely.

        WARNING: This permanently destroys the pod. Ensure all files
        have been uploaded to permanent storage before calling.
        """
        async with self._client() as client:
            response = await client.delete(f"{RUNPOD_API_BASE}/pods/{pod_id}")
            response.raise_for_status()

        logger.info(f"Terminated pod {pod_id}")
        return True

    async def get_pod_status(self, pod_id: str) -> PodStatus:
        """Get current status of a pod."""
        async with self._client() as client:
            response = await client.get(f"{RUNPOD_API_BASE}/pods/{pod_id}")
            response.raise_for_status()
            data = response.json()

        return PodStatus(
            id=pod_id,
            status=data.get("status", "UNKNOWN"),
            desired_status=data.get("desiredStatus", "UNKNOWN"),
            cost_per_hour=data.get("costPerHr", 0.0),
        )

    async def list_pods(self) -> list[Pod]:
        """List all pods for the account."""
        async with self._client() as client:
            response = await client.get(f"{RUNPOD_API_BASE}/pods")
            response.raise_for_status()
            pods_data = response.json()

        pods = []
        for data in pods_data if isinstance(pods_data, list) else []:
            pods.append(Pod(
                id=data.get("id", ""),
                name=data.get("name", ""),
                gpu_type=data.get("gpuTypeId", ""),
                status=data.get("status", ""),
                desired_status=data.get("desiredStatus", ""),
                cost_per_hour=data.get("costPerHr", 0.0),
                image_name=data.get("imageName", ""),
            ))
        return pods

    # ── Serverless Jobs ──

    async def submit_serverless_job(
        self,
        endpoint_id: str,
        input_data: dict[str, Any],
        timeout_ms: int = 300000,
    ) -> str:
        """Submit an async job to a serverless endpoint.

        Args:
            endpoint_id: The serverless endpoint ID.
            input_data: Job input payload.
            timeout_ms: Maximum execution time in milliseconds.

        Returns:
            Job ID for status tracking.
        """
        payload = {"input": input_data}

        async with self._client() as client:
            response = await client.post(
                f"{RUNPOD_SERVERLESS_BASE}/{endpoint_id}/run",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        job_id = data.get("id", "")
        logger.info(f"Submitted serverless job {job_id} to endpoint {endpoint_id}")
        return job_id

    async def submit_serverless_job_sync(
        self,
        endpoint_id: str,
        input_data: dict[str, Any],
        timeout_seconds: int = 60,
    ) -> JobStatus:
        """Submit a synchronous job that waits for completion.

        Args:
            endpoint_id: The serverless endpoint ID.
            input_data: Job input payload.
            timeout_seconds: Maximum wait time.

        Returns:
            JobStatus with output data.
        """
        payload = {"input": input_data}

        async with httpx.AsyncClient(
            headers=self._headers,
            timeout=float(timeout_seconds + 10),
        ) as client:
            response = await client.post(
                f"{RUNPOD_SERVERLESS_BASE}/{endpoint_id}/runsync",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return JobStatus(
            id=data.get("id", ""),
            status=data.get("status", ""),
            output=data.get("output"),
            execution_time_ms=data.get("executionTime", 0),
        )

    async def get_job_status(self, endpoint_id: str, job_id: str) -> JobStatus:
        """Check the status of a serverless job."""
        async with self._client() as client:
            response = await client.get(
                f"{RUNPOD_SERVERLESS_BASE}/{endpoint_id}/status/{job_id}"
            )
            response.raise_for_status()
            data = response.json()

        return JobStatus(
            id=job_id,
            status=data.get("status", "UNKNOWN"),
            output=data.get("output"),
            error=data.get("error"),
            execution_time_ms=data.get("executionTime", 0),
        )

    async def cancel_job(self, endpoint_id: str, job_id: str) -> bool:
        """Cancel a queued or in-progress serverless job."""
        async with self._client() as client:
            response = await client.post(
                f"{RUNPOD_SERVERLESS_BASE}/{endpoint_id}/cancel/{job_id}"
            )
            response.raise_for_status()

        logger.info(f"Cancelled job {job_id}")
        return True

    # ── Network Volumes ──

    async def list_network_volumes(self) -> list[Volume]:
        """List all network volumes."""
        async with self._client() as client:
            response = await client.get(f"{RUNPOD_API_BASE}/network-volumes")
            response.raise_for_status()
            volumes_data = response.json()

        volumes = []
        for data in volumes_data if isinstance(volumes_data, list) else []:
            volumes.append(Volume(
                id=data.get("id", ""),
                name=data.get("name", ""),
                size_gb=data.get("size", 0),
                datacenter_id=data.get("dataCenterId", ""),
            ))
        return volumes

    async def create_network_volume(self, name: str, size_gb: int, datacenter_id: str = "US-TX-3") -> Volume:
        """Create a network volume."""
        payload = {
            "name": name,
            "size": size_gb,
            "dataCenter": datacenter_id
        }
        async with self._client() as client:
            response = await client.post(f"{RUNPOD_API_BASE}/network-volumes", json=payload)
            response.raise_for_status()
            data = response.json()
            
        return Volume(
            id=data.get("id", ""),
            name=name,
            size_gb=size_gb,
            datacenter_id=datacenter_id
        )

    async def run_command_in_pod(self, pod_id: str, command: str) -> str:
        """Run a command inside a pod."""
        payload = {"command": command}
        async with self._client() as client:
            response = await client.post(f"{RUNPOD_API_BASE}/pods/{pod_id}/run", json=payload)
            response.raise_for_status()
            data = response.json()
            
        return data.get("output", "")

    # ── GPU Discovery ──

    async def get_gpu_types(self) -> list[GpuType]:
        """Get available GPU types and pricing."""
        async with self._client() as client:
            response = await client.get(f"{RUNPOD_API_BASE}/gpu-types")
            response.raise_for_status()
            gpu_data = response.json()

        gpu_types = []
        for data in gpu_data if isinstance(gpu_data, list) else []:
            gpu_types.append(GpuType(
                id=data.get("id", ""),
                display_name=data.get("displayName", ""),
                memory_gb=data.get("memoryInGb", 0),
                secure_cloud_price=data.get("secureCloud", {}).get("price", 0.0) if isinstance(data.get("secureCloud"), dict) else 0.0,
                community_cloud_price=data.get("communityCloud", {}).get("price", 0.0) if isinstance(data.get("communityCloud"), dict) else 0.0,
            ))
        return gpu_types

    # ── Health Check ──

    async def check_connection(self) -> bool:
        """Verify the API key is valid by listing pods."""
        try:
            async with self._client() as client:
                response = await client.get(f"{RUNPOD_API_BASE}/pods")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"RunPod connection check failed: {e}")
            return False

    async def check_endpoint_health(self, endpoint_id: str) -> dict[str, Any]:
        """Check health of a serverless endpoint."""
        try:
            async with self._client() as client:
                response = await client.get(
                    f"{RUNPOD_SERVERLESS_BASE}/{endpoint_id}/health"
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Endpoint health check failed: {e}")
            return {"status": "error", "message": str(e)}
