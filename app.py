
from flask import Flask, request, render_template_string
from network_checks import check_dns, check_tcp, check_http
from report import save_report

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NetDoctor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #101827;
            color: white;
            text-align: center;
            padding: 40px;
        }
        .container {
            max-width: 750px;
            margin: auto;
            background: #1e293b;
            padding: 30px;
            border-radius: 16px;
        }
        input {
            padding: 12px;
            width: 65%;
            border-radius: 8px;
            border: none;
        }
        button {
            padding: 12px 20px;
            background: #38bdf8;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        .result {
            background: #334155;
            padding: 15px;
            margin-top: 15px;
            border-radius: 10px;
            text-align: left;
        }
        .PASS { color: #4ade80; }
        .FAIL { color: #f87171; }
        .error { color: #fbbf24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🩺 NetDoctor</h1>
        <p>Automated Network and Service Diagnostics</p>
        <form method="POST">
            <input name="hostname"
                   placeholder="Enter hostname (example.com)"
                   value="{{ hostname }}" required>
            <button type="submit">Check Network</button>
        </form>

        {% if results %}
            <h2>Diagnostic Results</h2>
            {% for item in results %}
                <div class="result">
                    <h3>{{ item.check }}</h3>
                    <p class="{{ item.status }}">
                        Status: {{ item.status }}
                    </p>
                    <p>{{ item.message }}</p>
                    {% if item.suggestion %}
                        <p>Suggestion: {{ item.suggestion }}</p>
                    {% endif %}
                </div>
            {% endfor %}
            <h3>Overall Status: {{ overall }}</h3>
            <p>Report saved to diagnostic_report.json</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    hostname = ""
    overall = "NOT RUN"

    if request.method == "POST":
        hostname = request.form.get("hostname", "").strip()

        if hostname:
            try:
                dns = check_dns(hostname)
                tcp = check_tcp(hostname, 443)

                url = hostname
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url

                http = check_http(url)
                results = [dns, tcp, http]

                overall = (
                    "PASS" if all(
                        item.get("status") == "PASS"
                        for item in results
                    ) else "FAIL"
                )

                save_report(hostname, results)

            except Exception as e:
                results = [{
                    "check": "Diagnostic Error",
                    "status": "FAIL",
                    "message": str(e),
                    "suggestion": "Check the hostname and try again."
                }]
                overall = "FAIL"

    return render_template_string(
        HTML,
        hostname=hostname,
        results=results,
        overall=overall
    )

if __name__ == "__main__":
    app.run(debug=True)
