# src/analytics/wait_time.py

def calculate_waiting_time(arrival_rate: float,
                           service_rate: float,
                           epsilon: float = 0.01,
                           cap: float = 120.0) -> float:
    """
    W = 1 / max(μ - λ, ε)
    Bounded for stability.
    """

    effective_gap = max(service_rate - arrival_rate, epsilon)
    waiting_time = 1 / effective_gap

    return min(waiting_time, cap)
