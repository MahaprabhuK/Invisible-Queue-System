# src/analytics/confidence.py

def compute_decision_score(waiting_time: float,
                           threshold_time: float,
                           alpha: float = 1.0) -> float:
    """
    S = α (T_threshold − W)
    """
    return alpha * (threshold_time - waiting_time)


def evaluate_decision(score: float) -> str:
    """
    Decision rule
    """
    if score > 0:
        return "Worth Waiting"
    elif score < -20:
        return "System Overloaded"
    return "Not Worth Waiting"
