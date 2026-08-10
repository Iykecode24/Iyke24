import random
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# Core realism enhancement strings per requirements
REALISM_PROMPT = (
    "Photorealistic adult human subject, authentic human skin texture with visible pores and subtle natural imperfections, "
    "physically accurate anatomy, realistic eyes, individual hair strands, natural clothing physics, believable body weight and movement, "
    "realistic human walking speed, subtle breathing and blinking, natural environmental interaction, physically plausible lighting and shadows, "
    "professional live-action cinematography, realistic camera motion, temporal consistency, documentary-level environmental realism."
)

NEGATIVE_PROMPT = (
    "plastic skin, wax skin, artificial beauty filter, CGI appearance, game character appearance, rubber skin, malformed anatomy, "
    "extra fingers, distorted hands, unnatural motion, accelerated movement, floating objects, flickering, frame warping, "
    "duplicated people and inconsistent clothing, minor, child, age-ambiguous."
)

class DailyActivityEngine:
    """Intelligent Daily Activities System."""
    
    ACTIVITIES = {
        "Morning": [
            "waking up, opening curtains",
            "making coffee, preparing breakfast",
            "choosing clothes",
            "light exercise",
            "leaving home"
        ],
        "Daytime": [
            "walking through the city",
            "shopping",
            "café visit",
            "working",
            "sightseeing",
            "lunch",
            "driving/passenger scenes",
            "gym",
            "fashion shoot",
            "beach or park activities"
        ],
        "Evening": [
            "restaurant",
            "rooftop",
            "dinner",
            "event",
            "sunset walk",
            "getting ready",
            "fashion/lifestyle scenes"
        ],
        "Night": [
            "tasteful nightlife",
            "city lights",
            "lounge",
            "dancing",
            "social events",
            "arriving home"
        ]
    }
    
    @classmethod
    def get_time_of_day(cls) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "Morning"
        elif 11 <= hour < 17:
            return "Daytime"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
            
    @classmethod
    def generate_activity(cls, history: List[str] = None) -> str:
        """Generates an activity avoiding recent history if possible."""
        history = history or []
        time_of_day = cls.get_time_of_day()
        options = cls.ACTIVITIES[time_of_day]
        
        # Filter out recently used activities to avoid repetition
        available_options = [opt for opt in options if opt not in history[-5:]]
        
        if not available_options:
            available_options = options
            
        return random.choice(available_options)

class AutonomousContentDirector:
    """AI Content Director responsible for deciding what content should be produced."""
    
    @staticmethod
    def create_production_plan(model_profile: Any) -> Dict[str, Any]:
        """
        Takes an AI Model profile and generates a full 50-second scene plan.
        """
        history_log = model_profile.history_log or []
        recent_activities = [log.get("activity") for log in history_log]
        recent_wardrobes = [log.get("wardrobe") for log in history_log]
        
        # 1. Select Daily Activity
        activity = DailyActivityEngine.generate_activity(recent_activities)
        time_of_day = DailyActivityEngine.get_time_of_day()
        
        # 2. Select Wardrobe
        wardrobe = f"Stylish {time_of_day.lower()} outfit suitable for {activity}"
        
        # 3. Create Shot List for a 50-second video (5 shots of ~10 seconds)
        shot_list = [
            {"shot_number": 1, "duration": 10, "type": "medium shot", "action": f"Establishing shot of model {activity}"},
            {"shot_number": 2, "duration": 10, "type": "close-up", "action": "Subtle expression and realistic movement, natural blinking"},
            {"shot_number": 3, "duration": 10, "type": "tracking shot", "action": "Model moving naturally through the environment"},
            {"shot_number": 4, "duration": 10, "type": "full-body shot", "action": "Showing the full wardrobe and environment"},
            {"shot_number": 5, "duration": 10, "type": "slow push-in", "action": "Closing shot, realistic lighting interaction"}
        ]
        
        return {
            "model_id": str(model_profile.id),
            "activity": activity,
            "time_of_day": time_of_day,
            "wardrobe": wardrobe,
            "environment": f"Realistic {time_of_day} environment for {activity}",
            "music_category": "upbeat/lifestyle" if time_of_day in ["Daytime", "Evening"] else "chill/ambient",
            "shot_list": shot_list,
            "aspect_ratio": "9:16",
            "target_duration": 50
        }
        
    @staticmethod
    def enhance_prompt(base_prompt: str) -> Dict[str, str]:
        """Applies the mandatory realism profile to generation prompts."""
        return {
            "prompt": f"{base_prompt}, {REALISM_PROMPT}",
            "negative_prompt": NEGATIVE_PROMPT
        }
