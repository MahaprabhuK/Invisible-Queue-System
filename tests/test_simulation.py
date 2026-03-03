import unittest
from src.simulation.simulator import QueueSimulator

class TestQueueSimulator(unittest.TestCase):
    def test_initialization(self):
        sim = QueueSimulator(1.0, 2.0)
        self.assertEqual(sim.arrival_rate, 1.0)
        self.assertEqual(sim.service_rate, 2.0)
        self.assertEqual(sim.queue_length, 0)
        self.assertEqual(sim.current_time, 0)

    def test_step_logic_structure(self):
        # Using fixed rates since there is stochastic logic masked beneath generate_arrivals
        sim = QueueSimulator(0.0, 5.0) 
        # Zero arrivals, some services -> Queue length should stay 0
        q_len = sim.step()
        self.assertEqual(q_len, 0)
        
    def test_state_retrieval(self):
        sim = QueueSimulator(1.5, 2.0)
        state = sim.get_state()
        self.assertIn("time", state)
        self.assertIn("queue_length", state)
        self.assertEqual(state["time"], 0)

if __name__ == '__main__':
    unittest.main()
