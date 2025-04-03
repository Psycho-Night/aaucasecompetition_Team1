import unittest
import time

class TestExample(unittest.TestCase):
    def test_fast(self):
        self.assertEqual(1 + 1, 2)

    def test_slow(self):
        time.sleep(3)  # Simulating a slow test
        self.assertTrue(True)

def run_tests():
    start_time = time.time()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExample)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    end_time = time.time()

    print(f"Total Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    run_tests()
