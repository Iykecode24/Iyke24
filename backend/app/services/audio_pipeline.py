import asyncio
import logging
from typing import List, Optional
import os

logger = logging.getLogger(__name__)

class AudioPipeline:
    def __init__(self):
        """Initialize the AudioPipeline."""
        pass

    async def overlay_audio(
        self,
        video_path: str,
        voiceover_paths: List[str],
        bgm_path: Optional[str],
        output_path: str,
        bgm_volume: float = 0.2
    ) -> str:
        """
        Overlay background music and voiceover tracks onto a video.
        Applies audio normalization using FFmpeg filters.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        inputs = ["-i", video_path]
        
        # Add voiceovers
        for vo_path in voiceover_paths:
            inputs.extend(["-i", vo_path])
            
        # Add bgm
        if bgm_path:
            inputs.extend(["-i", bgm_path])

        filter_complex = ""
        audio_streams = []

        # Assuming input 0 is video. It might have audio. We will ignore its audio and use voiceovers + bgm.
        # If we need to keep original video audio, we would include [0:a]. For now, we only use VO + BGM.
        
        input_idx = 1
        
        for i in range(len(voiceover_paths)):
            # Normalize voiceover audio (loudnorm)
            filter_complex += f"[{input_idx}:a]loudnorm=I=-16:TP=-1.5:LRA=11[vo{i}];"
            audio_streams.append(f"[vo{i}]")
            input_idx += 1
            
        if bgm_path:
            # Lower volume of BGM and normalize
            filter_complex += f"[{input_idx}:a]volume={bgm_volume},loudnorm=I=-20:TP=-2.0:LRA=11[bgm];"
            audio_streams.append("[bgm]")
            input_idx += 1
            
        if not audio_streams:
            # If no audio to overlay, just copy the video
            cmd = ["ffmpeg", "-y", "-i", video_path, "-c", "copy", output_path]
            return await self._run_ffmpeg(cmd, output_path)

        # Mix all audio streams
        mix_inputs = "".join(audio_streams)
        filter_complex += f"{mix_inputs}amix=inputs={len(audio_streams)}:duration=first:dropout_transition=2[aout]"

        cmd = [
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]

        return await self._run_ffmpeg(cmd, output_path)

    async def _run_ffmpeg(self, cmd: List[str], output_path: str) -> str:
        """Run an FFmpeg command asynchronously."""
        logger.info(f"Running FFmpeg (AudioPipeline): {' '.join(cmd)}")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg audio pipeline failed: {stderr.decode()}")
        return output_path
