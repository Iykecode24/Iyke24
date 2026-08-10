from typing import List, Dict, Any, TypeVar, Type
from pydantic import BaseModel, ValidationError
import logging
from app.providers.openai.structured_output import generate_structured_output

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class Agent:
    def __init__(self, name: str, role: str, system_prompt: str, model: str = "gpt-4o", max_loops: int = 3):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.model = model
        self.max_loops = max_loops

class MultiAgentOrchestrator:
    """
    Manages structured agents (e.g., Creative Director, Editor, Lip-Sync Director),
    enforcing loop limits and Pydantic validation for outputs.
    """
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        # Initialize the 20 structured agents
        agent_definitions = [
            ("Creative Director", "Oversees the entire creative vision of the movie.", "You are the Creative Director. Ensure the output aligns with the movie's vision."),
            ("Editor", "Assembles clips and ensures smooth transitions.", "You are the Editor. Ensure pacing and clip transitions are logical."),
            ("Lip-Sync Director", "Ensures audio matches visual lip movements.", "You are the Lip-Sync Director. Make sure the dialogue matches the generated clips."),
            ("Screenwriter", "Writes the dialogue and scene descriptions.", "You are the Screenwriter. Produce high-quality scripts."),
            ("Casting Director", "Selects the best visual and voice matches for characters.", "You are the Casting Director."),
            ("Cinematographer", "Determines camera angles, lighting, and composition.", "You are the Cinematographer."),
            ("Sound Designer", "Manages sound effects and background music.", "You are the Sound Designer."),
            ("Music Supervisor", "Selects or creates the score for the project.", "You are the Music Supervisor."),
            ("Art Director", "Manages the visual style and aesthetic.", "You are the Art Director."),
            ("Costume Designer", "Designs character clothing and accessories.", "You are the Costume Designer."),
            ("Makeup & Hair Stylist", "Designs character makeup and hair.", "You are the Makeup & Hair Stylist."),
            ("VFX Supervisor", "Oversees visual effects integration.", "You are the VFX Supervisor."),
            ("Colorist", "Grades the footage for the final look.", "You are the Colorist."),
            ("Foley Artist", "Creates everyday sound effects.", "You are the Foley Artist."),
            ("Voice Director", "Directs the AI voice actors for emotional delivery.", "You are the Voice Director."),
            ("Continuity Supervisor", "Ensures consistency across scenes.", "You are the Continuity Supervisor."),
            ("Location Scout", "Determines the settings for each scene.", "You are the Location Scout."),
            ("Title Designer", "Creates opening and closing credits.", "You are the Title Designer."),
            ("Marketing Director", "Creates promotional materials and trailers.", "You are the Marketing Director."),
            ("Producer", "Manages budget, timeline, and final approvals.", "You are the Producer.")
        ]
        
        for name, role, prompt in agent_definitions:
            self.agents[name] = Agent(name=name, role=role, system_prompt=prompt)

    async def execute_task(self, agent_name: str, task_prompt: str, response_model: Type[T]) -> T:
        """
        Executes a task with a specific agent, enforcing loop limits and strict Pydantic validation.
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found.")
            
        agent = self.agents[agent_name]
        
        messages = [
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": task_prompt}
        ]
        
        loop_count = 0
        last_error = None
        
        while loop_count < agent.max_loops:
            try:
                loop_count += 1
                logger.info(f"Agent {agent.name} executing loop {loop_count}/{agent.max_loops}")
                
                # generate_structured_output inherently uses OpenAI's structured outputs feature
                # which guarantees the output conforms to the Pydantic schema
                result = await generate_structured_output(
                    model=agent.model,
                    messages=messages,
                    response_model=response_model
                )
                
                # We return the Pydantic model directly as validation is handled by openai's parse
                return result
                
            except ValidationError as e:
                last_error = e
                logger.warning(f"Validation error in loop {loop_count}: {e}")
                # Append the error to messages to allow the agent to correct itself
                messages.append({"role": "assistant", "content": "The generated output failed validation."})
                messages.append({"role": "user", "content": f"Please correct the following validation errors: {e}"})
            except Exception as e:
                last_error = e
                logger.error(f"Unexpected error in loop {loop_count}: {e}")
                break
                
        raise RuntimeError(f"Agent '{agent.name}' failed to produce valid output after {agent.max_loops} loops. Last error: {last_error}")
