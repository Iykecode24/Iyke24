import logging
from typing import List

from app.integrations.runpod_client import RunPodClient

logger = logging.getLogger(__name__)

class RunPodSetup:
    """
    Handles auto-installation of dependencies and workflows on RunPod GPU instances.
    """
    def __init__(self, client: RunPodClient):
        self.client = client

    async def run_setup(self, pod_id: str) -> None:
        """
        Executes the auto-installation scripts on the pod.
        """
        logger.info(f"Starting auto-setup for pod {pod_id}")
        
        await self.install_ffmpeg(pod_id)
        await self.install_comfyui_and_deps(pod_id)
        await self.install_custom_workflows(pod_id)
        
        logger.info(f"Auto-setup completed for pod {pod_id}")

    async def install_ffmpeg(self, pod_id: str) -> None:
        """
        Auto-installs FFmpeg.
        """
        logger.info(f"Installing FFmpeg on pod {pod_id}")
        script = "apt-get update && apt-get install -y ffmpeg"
        await self.client.run_command_in_pod(pod_id, script)

    async def install_comfyui_and_deps(self, pod_id: str) -> None:
        """
        Auto-installs ComfyUI, PyTorch, and xFormers.
        """
        logger.info(f"Installing ComfyUI, PyTorch, and xFormers on pod {pod_id}")
        script = (
            "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && "
            "pip install xformers && "
            "cd /workspace && "
            "if [ ! -d 'ComfyUI' ]; then git clone https://github.com/comfyanonymous/ComfyUI.git; fi && "
            "cd ComfyUI && "
            "pip install -r requirements.txt"
        )
        await self.client.run_command_in_pod(pod_id, script)

    async def install_custom_workflows(self, pod_id: str) -> None:
        """
        Auto-installs Iyke Studio custom workflows.
        """
        logger.info(f"Installing Iyke Studio custom workflows on pod {pod_id}")
        # Placeholder for downloading/copying custom workflows to the volume
        script = (
            "mkdir -p /workspace/comfyui/custom_nodes/iyke_workflows && "
            "echo 'Downloading custom workflows...' && "
            "wget -qO /workspace/comfyui/custom_nodes/iyke_workflows/workflow.json https://example.com/iyke_workflow.json || true"
        )
        await self.client.run_command_in_pod(pod_id, script)
