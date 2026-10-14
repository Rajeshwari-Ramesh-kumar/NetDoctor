import unittest
from network_checks import check_dns, check_tcp, check_http


class TestNetworkChecks(unittest.TestCase):

    def test_dns_returns_result(self):
        result = check_dns("example.com")

        self.assertIn("status", result)
        self.assertIn(result["status"], ["PASS", "FAIL"])

    def test_tcp_returns_result(self):
        result = check_tcp("example.com", 443)

        self.assertIn("status", result)
        self.assertIn(result["status"], ["PASS", "FAIL"])

    def test_http_returns_result(self):
        result = check_http("https://example.com")

        self.assertIn("status", result)
        self.assertIn(result["status"], ["PASS", "FAIL"])


if __name__ == "__main__":
    unittest.main()