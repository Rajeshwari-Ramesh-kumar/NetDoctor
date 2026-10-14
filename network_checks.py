
import socket


def check_dns(hostname):
    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )

        ip_addresses = sorted(set(
            result[4][0] for result in results
        ))

        if ip_addresses:
            return {
                "check": "DNS Resolution",
                "status": "PASS",
                "hostname": hostname,
                "ip_addresses": ip_addresses,
                "message": "DNS resolution successful",
                "suggestion": "No DNS issue detected."
            }

        return {
            "check": "DNS Resolution",
            "status": "FAIL",
            "hostname": hostname,
            "ip_addresses": [],
            "message": "No IPv4 address found",
            "suggestion": "Check the hostname and DNS configuration."
        }

    except socket.gaierror:
        return {
            "check": "DNS Resolution",
            "status": "FAIL",
            "hostname": hostname,
            "ip_addresses": [],
            "message": "Hostname could not be resolved",
            "suggestion": (
                "Check the hostname, internet connection, "
                "and DNS settings."
            )
        }

        
def check_tcp(hostname, port, timeout=3):
    import socket
    import time

    start_time = time.perf_counter()

    try:
        with socket.create_connection(
            (hostname, port), timeout=timeout
        ):
            elapsed = round(
                (time.perf_counter() - start_time) * 1000, 2
            )

            return {
                "check": "TCP Connectivity",
                "status": "PASS",
                "hostname": hostname,
                "port": port,
                "response_time_ms": elapsed,
                "message": "TCP connection successful",
                "suggestion": "No TCP connectivity issue detected."
            }

    except (socket.timeout, TimeoutError):
        return {
            "check": "TCP Connectivity",
            "status": "FAIL",
            "hostname": hostname,
            "port": port,
            "response_time_ms": None,
            "message": "Connection timed out",
            "suggestion": (
                "Check network connectivity, firewall rules, "
                "and whether the service is running."
            )
        }

    except OSError as error:
        return {
            "check": "TCP Connectivity",
            "status": "FAIL",
            "hostname": hostname,
            "port": port,
            "response_time_ms": None,
            "message": str(error),
            "suggestion": (
                "Verify the port number, firewall settings, "
                "and whether the server accepts connections."
            )
        }

import urllib.request
import urllib.error
import time


def check_http(url, timeout=5):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "NetworkDiagnostics/1.0"},
        method="GET"
    )

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request, timeout=timeout
        ) as response:
            elapsed = round(
                (time.perf_counter() - start_time) * 1000, 2
            )

            status_code = response.status

            return {
                "check": "HTTP Response",
                "status": (
                    "PASS" if 200 <= status_code < 400 else "FAIL"
                ),
                "url": url,
                "http_status_code": status_code,
                "response_time_ms": elapsed,
                "message": "HTTP request completed",
                "suggestion": (
                    "No HTTP issue detected."
                    if 200 <= status_code < 400
                    else "Check the server response and URL."
                )
            }

    except urllib.error.HTTPError as error:
        elapsed = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        return {
            "check": "HTTP Response",
            "status": "FAIL",
            "url": url,
            "http_status_code": error.code,
            "response_time_ms": elapsed,
            "message": str(error),
            "suggestion": (
                "Check the HTTP status code, requested URL, "
                "and server configuration."
            )
        }

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {
            "check": "HTTP Response",
            "status": "FAIL",
            "url": url,
            "http_status_code": None,
            "response_time_ms": None,
            "message": str(error),
            "suggestion": (
                "Check internet connectivity, DNS, server availability, "
                "and firewall settings."
            )
        }

