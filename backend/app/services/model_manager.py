import logging
from typing import List, Dict

from app.integrations.runpod_client import RunPodClient

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages AI models on the RunPod network volume, ensuring they are downloaded
    and ready for use without duplication.
    """
    def __init__(self, client: RunPodClient):
        self.client = client
        # Dictionary of model names to their download URLs and target paths on the volume
        self.required_models = {
            "HunyuanVideo": {
                "url": "https://huggingface.co/Tencent/HunyuanVideo/resolve/main/hunyuan_video_model.safetensors",
                "path": "/workspace/models/checkpoints/hunyuan_video_model.safetensors"
            },
            "FLUX": {
                "url": "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors",
                "path": "/workspace/models/checkpoints/flux1-schnell.safetensors"
            }
        }

    async def ensure_models(self, pod_id: str) -> None:
        """
        Checks for missing models and downloads them directly to the network volume.
        """
        logger.info(f"Checking for required models on pod {pod_id}...")
        
        for model_name, model_info in self.required_models.items():
            url = model_info["url"]
            path = model_info["path"]
            
            # Bash script to check if file exists and has size > 0, otherwise download
            script = (
                f"if [ ! -s {path} ]; then "
                f"echo 'Downloading {model_name}...' && "
                f"wget -qO {path} {url}; "
                f"else "
                f"echo '{model_name} already exists.'; "
                f"fi"
            )
            
            output = await self.client.run_command_in_pod(pod_id, script)
            logger.info(f"Model {model_name} check: {output.strip()}")

        logger.info("All models checked.")
