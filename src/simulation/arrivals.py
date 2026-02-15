# src/simulation/arrivals.py

import numpy as np


def generate_arrivals(arrival_rate: float) -> int:
    """
    Generate arrivals using Poisson distribution.
    """
    return np.random.poisson(arrival_rate)


def generate_services(service_rate: float) -> int:
    """
    Generate completed services using Poisson distribution.
    """
    return np.random.poisson(service_rate)
