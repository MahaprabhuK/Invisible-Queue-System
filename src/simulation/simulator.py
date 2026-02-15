# src/simulation/simulator.py

from simulation.arrivals import generate_arrivals, generate_services


class QueueSimulator:
    def __init__(self, arrival_rate: float, service_rate: float):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.queue_length = 0
        self.current_time = 0

    def step(self) -> int:
        """
        Perform one simulation step.
        """
        arrivals = generate_arrivals(self.arrival_rate)
        services = generate_services(self.service_rate)

        self.queue_length += arrivals
        self.queue_length = max(0, self.queue_length - services)

        self.current_time += 1
        return self.queue_length

    def get_state(self):
        return {
            "time": self.current_time,
            "queue_length": self.queue_length
        }
