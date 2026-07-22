import unittest

from provider_benchmark import percentile, request_payload, summarize


class ProviderBenchmarkTests(unittest.TestCase):
    def test_percentile(self):
        self.assertEqual(percentile([10, 20, 30, 40], 0.95), 40)

    def test_payload(self):
        self.assertEqual(request_payload("m", "hello")["messages"][0]["content"], "hello")

    def test_summary(self):
        report = summarize({"name": "p", "model": "m"}, [{"ok": True, "latency_ms": 10}, {"ok": False, "latency_ms": 3}])
        self.assertEqual(report["success_rate"], 0.5)
        self.assertEqual(report["latency_ms"]["mean"], 10)


if __name__ == "__main__":
    unittest.main()
