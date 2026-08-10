class CostEstimate:
    pass
class UsageSummary:
    pass

def estimate_project_cost(project) -> CostEstimate:
    return CostEstimate()

def check_cost_limits(user_id: str, estimated_cost: float) -> bool:
    return True

def record_cost(project_id: str, category: str, amount: float):
    pass

def get_usage_summary(user_id: str, period: str) -> UsageSummary:
    return UsageSummary()

def check_cost_alerts(user_id: str):
    pass
