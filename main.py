
from network_checks import check_dns, check_tcp, check_http
from report import save_report

print("===================================")
print(" AUTOMATED NETWORK DIAGNOSTICS")
print("===================================")

hostname = input("Enter a website hostname: ").strip()

# DNS check
dns = check_dns(hostname)

print("\n--- DNS DIAGNOSTIC RESULT ---")
print("Status:", dns["status"])
print("Message:", dns["message"])

if dns["ip_addresses"]:
    print("IP Addresses:", ", ".join(dns["ip_addresses"]))

print("Suggestion:", dns["suggestion"])

# TCP check
tcp = check_tcp(hostname, 443)

print("\n--- TCP DIAGNOSTIC RESULT ---")
print("Status:", tcp["status"])
print("Port:", tcp["port"])
print("Message:", tcp["message"])

if tcp["response_time_ms"] is not None:
    print("Connection Time (ms):", tcp["response_time_ms"])

print("Suggestion:", tcp["suggestion"])

# HTTP check
http = check_http(hostname)

print("\n--- HTTP DIAGNOSTIC RESULT ---")
print("Status:", http["status"])
print("HTTP Status Code:", http["http_status_code"])
print("Response Time (ms):", http["response_time_ms"])
print("Message:", http["message"])
print("Suggestion:", http["suggestion"])
results = [dns, tcp, http]
passed_checks = sum(
    1 for item in results
    if item["status"] == "PASS"
)

health_score = (passed_checks / len(results)) * 100

print("\n========== NETWORK HEALTH ==========")
print("Health Score:", round(health_score), "%")

if health_score == 100:
    print("Overall Status: HEALTHY")
elif health_score >= 50:
    print("Overall Status: PARTIALLY HEALTHY")
else:
    print("Overall Status: UNHEALTHY")

print("===================================")
save_report(hostname, results)