from flask import Flask, jsonify, render_template_string
from pathlib import Path
import json

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sample_data.json"

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PySpark Data Viewer</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 24px; background: #f3f6fb; }
      table { width: 100%; border-collapse: collapse; background: white; }
      th, td { border: 1px solid #dfe5ef; padding: 10px; text-align: left; }
      th { background: #eaf1ff; }
      h1 { margin-bottom: 12px; }
      .status { margin-bottom: 16px; font-weight: bold; }
    </style>
  </head>
  <body>
    <h1>PySpark Sample Data</h1>
    <div class="status" id="status">Loading data...</div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th>Salary</th>
          <th>City</th>
        </tr>
      </thead>
      <tbody id="data-body"></tbody>
    </table>

    <script>
      async function loadData() {
        const response = await fetch('/api/data');
        const data = await response.json();
        const tbody = document.getElementById('data-body');
        const status = document.getElementById('status');

        tbody.innerHTML = data.map(row => `
          <tr>
            <td>${row.name}</td>
            <td>${row.department}</td>
            <td>$${Number(row.salary).toLocaleString()}</td>
            <td>${row.city}</td>
          </tr>
        `).join('');

        status.textContent = `Loaded ${data.length} records`;
      }

      loadData();
    </script>
  </body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/data")
def api_data():
    if not DATA_FILE.exists():
        return jsonify([])

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return jsonify(json.load(file))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
