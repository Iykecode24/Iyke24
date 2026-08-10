from typing import List, Optional

class ContentCheckResult:
    is_safe: bool
    flagged_reasons: List[str]

def check_text_safety(text: str) -> ContentCheckResult:
    blocked_words = ["violence", "terrorism", "hate"]
    reasons = [w for w in blocked_words if w in text.lower()]
    result = ContentCheckResult()
    result.is_safe = len(reasons) == 0
    result.flagged_reasons = reasons
    return result

def check_consent_required(content_type: str) -> bool:
    return content_type in ["deepfake", "voice_clone"]

def flag_content(project_id: str, content: str, reason: str):
    pass
