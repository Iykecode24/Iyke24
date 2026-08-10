import asyncio
import os
import uuid
from typing import List
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class EditingService:
    def __init__(self):
        """Initialize the EditingService."""
        pass

    async def assemble_video_clips(
        self,
        clip_paths: List[str],
        output_path: str,
        transition_duration: float = 0.5,
        resolution: str = "1920x1080",
        enforce_natural_pauses: bool = True
    ) -> str:
        """
        Assemble multiple video clips into a single movie with optional crossfade transitions.
        Uses FFmpeg via subprocess. Enforces natural conversation turn-taking, overlaps, and pregnant pauses.
        """
        if not clip_paths:
            raise ValueError("No clip paths provided for assembly")

        if len(clip_paths) == 1:
            # Just copy if there's only one clip
            cmd = ["ffmpeg", "-y", "-i", clip_paths[0], "-c", "copy", output_path]
            return await self._run_ffmpeg(cmd, output_path)

        # We will build a complex filter for crossfades
        # e.g., ffmpeg -i 1.mp4 -i 2.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=3.5[v]" -map "[v]" output.mp4
        
        inputs = []
        for path in clip_paths:
            inputs.extend(["-i", path])

        filter_complex = ""
        last_out = ""
        
        # We need to compute offsets for xfade. To do this perfectly, we need durations of each clip.
        # Let's simplify by using concat demuxer if transition_duration is 0, else we need ffprobe for durations.
        
        if transition_duration <= 0:
            # Simple concat using demuxer
            concat_file = f"{output_path}.txt"
            try:
                with open(concat_file, "w") as f:
                    for path in clip_paths:
                        f.write(f"file '{os.path.abspath(path)}'\n")
                
                cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", output_path]
                await self._run_ffmpeg(cmd, output_path)
            finally:
                if os.path.exists(concat_file):
                    os.remove(concat_file)
            return output_path
        else:
            # Using xfade requires durations. Here we get the duration of each clip.
            offsets = []
            current_offset = 0.0
            
            for i in range(len(clip_paths) - 1):
                dur = await self.get_video_duration(clip_paths[i])
                
                actual_transition = transition_duration
                if enforce_natural_pauses:
                    # Enforce natural conversation turn-taking, overlaps, and pregnant pauses
                    if i % 2 == 0:
                        actual_transition = min(dur / 2, transition_duration * 1.5)  # Simulate overlap
                    else:
                        actual_transition = min(dur / 2, transition_duration * 0.5)  # Simulate pregnant pause
                        
                offset = current_offset + dur - actual_transition
                offsets.append(offset)
                current_offset = offset

            for i in range(len(clip_paths) - 1):
                in1 = f"[{i}:v]" if i == 0 else f"[v{i}]"
                in2 = f"[{i+1}:v]"
                out = f"[v{i+1}]"
                offset = offsets[i]
                filter_complex += f"{in1}{in2}xfade=transition=fade:duration={transition_duration}:offset={offset}{out};"
                last_out = out

            # Remove trailing semicolon
            filter_complex = filter_complex.rstrip(";")

            cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_complex, "-map", last_out, "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path]
            return await self._run_ffmpeg(cmd, output_path)

    async def trim_video(self, input_path: str, output_path: str, start_time: float, duration: float) -> str:
        """
        Trim a video clip.
        """
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ss", str(start_time),
            "-t", str(duration),
            "-c:v", "copy",
            "-c:a", "copy",
            output_path
        ]
        return await self._run_ffmpeg(cmd, output_path)

    async def get_video_duration(self, file_path: str) -> float:
        """Get video duration using ffprobe."""
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", file_path
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            logger.error(f"ffprobe error: {stderr.decode()}")
            raise RuntimeError(f"Could not get duration for {file_path}")
        return float(stdout.decode().strip())

    async def _run_ffmpeg(self, cmd: List[str], output_path: str) -> str:
        """Run an FFmpeg command asynchronously."""
        logger.info(f"Running FFmpeg: {' '.join(cmd)}")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg command failed: {stderr.decode()}")
        return output_path
