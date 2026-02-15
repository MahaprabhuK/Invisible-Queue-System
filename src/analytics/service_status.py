# src/analytics/service_status.py

def calculate_utilization(arrival_rate: float,
                          service_rate: float) -> float:
    """
    ρ = λ / μ
    """
    if service_rate == 0:
        return 0.0

    return arrival_rate / service_rate
