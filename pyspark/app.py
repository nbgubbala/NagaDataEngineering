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
      body {
        font-family: Arial, sans-serif;
        margin: 24px;
        background: #f3f6fb;
        color: #1f2937;
      }
      h1 { margin-bottom: 12px; }
      .toolbar {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin: 16px 0 20px;
        align-items: center;
      }
      .toolbar input, .toolbar select {
        padding: 10px 12px;
        border: 1px solid #ced6e4;
        border-radius: 8px;
        font-size: 14px;
      }
      .summary {
        display: grid;
        grid-template-columns: repeat(3, minmax(150px, 1fr));
        gap: 12px;
        margin-bottom: 18px;
      }
      .card {
        background: white;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      }
      .card-label {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 6px;
      }
      .card-value {
        font-size: 24px;
        font-weight: bold;
      }
      .chart {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      }
      .bar-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 8px 0;
      }
      .bar-label {
        width: 110px;
        font-size: 12px;
      }
      .bar-track {
        flex: 1;
        background: #e5e7eb;
        border-radius: 999px;
        height: 12px;
        overflow: hidden;
      }
      .bar-fill {
        background: linear-gradient(90deg, #4f46e5, #22c55e);
        height: 100%;
        border-radius: 999px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      }
      th, td {
        border: 1px solid #dfe3ec;
        padding: 10px 12px;
        text-align: left;
      }
      th { background: #e5eefc; }
      .status { margin-bottom: 16px; font-weight: 600; }
    </style>
  </head>
  <body>
    <h1>PySpark Sample Data</h1>
    <div class="status" id="status">Loading data...</div>

    <div class="toolbar">
      <input id="search" type="text" placeholder="Search name or department" />
      <select id="cityFilter">
        <option value="all">All cities</option>
      </select>
      <select id="sortBy">
        <option value="name">Sort by name</option>
        <option value="salary-desc">Salary: high to low</option>
        <option value="salary-asc">Salary: low to high</option>
        <option value="city">City</option>
      </select>
    </div>

    <div class="summary">
      <div class="card">
        <div class="card-label">Employees</div>
        <div class="card-value" id="totalCount">0</div>
      </div>
      <div class="card">
        <div class="card-label">Average Salary</div>
        <div class="card-value" id="avgSalary">$0</div>
      </div>
      <div class="card">
        <div class="card-label">Top City</div>
        <div class="card-value" id="topCity">-</div>
      </div>
    </div>

    <div class="chart" id="chart"></div>

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
      let allData = [];

      function formatCurrency(value) {
        return `$${Number(value).toLocaleString()}`;
      }

      function updateSummary(data) {
        const total = data.length;
        const avg = total ? data.reduce((sum, row) => sum + Number(row.salary), 0) / total : 0;
        const cityCounts = {};

        data.forEach(row => {
          const city = row.city;
          cityCounts[city] = (cityCounts[city] || 0) + 1;
        });

        const topCity = Object.entries(cityCounts).sort((a, b) => b[1] - a[1])[0];

        document.getElementById('totalCount').textContent = total;
        document.getElementById('avgSalary').textContent = formatCurrency(avg);
        document.getElementById('topCity').textContent = topCity ? topCity[0] : '-';
      }

      function renderChart(data) {
        const chart = document.getElementById('chart');
        const cityTotals = {};

        data.forEach(row => {
          cityTotals[row.city] = (cityTotals[row.city] || 0) + Number(row.salary);
        });

        const entries = Object.entries(cityTotals).slice(0, 5);
        const max = entries.length ? Math.max(...entries.map(([, value]) => value)) : 1;

        chart.innerHTML = entries.length
          ? entries.map(([city, total]) => `
              <div class="bar-row">
                <div class="bar-label">${city}</div>
                <div class="bar-track">
                  <div class="bar-fill" style="width: ${(total / max) * 100}%"></div>
                </div>
                <div>${formatCurrency(total)}</div>
              </div>
            `).join('')
          : '<div>No data available</div>';
      }

      function applyFilters() {
        const searchTerm = document.getElementById('search').value.trim().toLowerCase();
        const selectedCity = document.getElementById('cityFilter').value;
        const sortBy = document.getElementById('sortBy').value;

        let filtered = [...allData].filter(row => {
          const matchesSearch = !searchTerm || row.name.toLowerCase().includes(searchTerm) || row.department.toLowerCase().includes(searchTerm);
          const matchesCity = selectedCity === 'all' || row.city === selectedCity;
          return matchesSearch && matchesCity;
        });

        if (sortBy === 'salary-desc') {
          filtered.sort((a, b) => Number(b.salary) - Number(a.salary));
        } else if (sortBy === 'salary-asc') {
          filtered.sort((a, b) => Number(a.salary) - Number(b.salary));
        } else if (sortBy === 'city') {
          filtered.sort((a, b) => a.city.localeCompare(b.city));
        } else {
          filtered.sort((a, b) => a.name.localeCompare(b.name));
        }

        renderTable(filtered);
        updateSummary(filtered);
        renderChart(filtered);
      }

      function renderTable(data) {
        const tbody = document.getElementById('data-body');
        tbody.innerHTML = data.map(row => `
          <tr>
            <td>${row.name}</td>
            <td>${row.department}</td>
            <td>${formatCurrency(row.salary)}</td>
            <td>${row.city}</td>
          </tr>
        `).join('');
      }

      async function loadData() {
        const response = await fetch('/api/data');
        allData = await response.json();

        const citySelect = document.getElementById('cityFilter');
        const cities = Array.from(new Set(allData.map(row => row.city))).sort();
        citySelect.innerHTML = '<option value="all">All cities</option>' +
          cities.map(city => `<option value="${city}">${city}</option>`).join('');

        document.getElementById('search').addEventListener('input', applyFilters);
        document.getElementById('cityFilter').addEventListener('change', applyFilters);
        document.getElementById('sortBy').addEventListener('change', applyFilters);

        applyFilters();
        document.getElementById('status').textContent = `Loaded ${allData.length} records`;
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
