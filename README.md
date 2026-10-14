# NetDoctor – Automated Network and Service Diagnostics

## Project Description
NetDoctor is a Python-based network diagnostic application that checks website connectivity and helps identify basic network-related issues.

The application performs DNS resolution, TCP connectivity, and HTTP response checks. It displays diagnostic results and provides troubleshooting suggestions.

## Features
- DNS resolution check
- TCP connectivity check on port 443
- HTTP response check
- PASS and FAIL status display
- Troubleshooting suggestions
- Diagnostic report generation in JSON format
- Automated testing using Python unittest
- Web interface built using Flask

## Technologies Used
- Python
- Flask
- Socket
- urllib
- JSON
- unittest
- HTML and CSS

## Project Files
- `app.py` – Runs the web application.
- `main.py` – Runs the command-line diagnostic program.
- `network_checks.py` – Contains DNS, TCP, and HTTP diagnostic functions.
- `report.py` – Generates the JSON diagnostic report.
- `test_network_checks.py` – Contains automated tests.
- `diagnostic_report.json` – Stores the diagnostic results.

## Installation

1. Install Python 3.
2. Open the project folder in VS Code.
3. Install Flask:

```bash
python -m pip install flask
```

## Run the Web Application

```bash
python app.py
```

Open this address in your browser:

`http://127.0.0.1:5000`

Enter a hostname such as `example.com` and click **Check Network**.

## Run Automated Tests

```bash
python -m unittest -v
```

## Test Cases
- Valid hostname: `example.com`
- Invalid hostname: `this-domain-123456789.invalid`

The results depend on network connectivity and the target service response.

## Limitations
This is a basic diagnostic application. It currently checks TCP connectivity on port 443 and does not identify every possible network issue.

## Future Enhancements
- Support for user-selected ports
- More diagnostic test cases
- Diagnostic history and timestamps
- Downloadable reports
- Enhanced troubleshooting recommendations

## Author
Team VisionVerse

## Event
Dev Sprint'26
