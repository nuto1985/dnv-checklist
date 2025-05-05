
from flask import Flask, render_template_string, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Load checklist data from external JSON
with open("checklist_data.json") as f:
    checklist_data = json.load(f)

SAVE_FILE = "responses.json"

def load_responses():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_responses(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

@app.route('/')
def index():
    responses = load_responses()
    status = {}
    for sec, secdata in checklist_data.items():
        answered = responses.get(sec, {})
        count = sum(1 for i in secdata["items"] if answered.get(i, {}).get("check"))
        status[sec] = f"{count}/{len(secdata['items'])}"
    return render_template_string("""
    <html>
    <head>
        <title>DNV Checklist Dashboard</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; }
            td, th { padding: 8px 12px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>📋 DNV-ST-0145 Chapter 9 Compliance Dashboard</h1>
        <p>Welcome! This tool helps you track your compliance with Chapter 9 of the DNV-ST-0145 standard.</p>
        <p>To get started, click a section below to complete the checklist. Your progress will be saved automatically.</p>
    <p>
        <a href="/export/csv">📊 Export CSV</a> |
        <a href="#" onclick="window.print()">🖨 Print Page</a>
    </p>
        <table>
            <tr><th>Section</th><th>Status</th><th>Action</th></tr>
            {% for section, stat in status.items() %}
            <tr>
                <td>{{ checklist_data[section]["title"] }}</td>
                <td>{{ stat }}</td>
                <td><a href="{{ url_for('checklist', section=section) }}">Edit</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, checklist_data=checklist_data, status=status)

@app.route('/checklist/<section>', methods=['GET', 'POST'])
def checklist(section):
    section_data = checklist_data.get(section, {})
    items = section_data.get("items", [])
    section_title = section_data.get("title", "")
    responses = load_responses()

    if request.method == 'POST':
        form_data = {item: {"check": f"{item}_check" in request.form, "comment": request.form.get(f"{item}_comment", "")} for item in items}
        responses[section] = form_data
        save_responses(responses)
        return redirect(url_for('index'))

    saved_data = responses.get(section, {})
    return render_template_string("""
    <html>
    <head>
        <title>Checklist {{ section }}</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            label { display: block; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h2>{{ section_title }}</h2>
        <form method="post">
            {% for item in items %}
                <label><input type="checkbox" name="{{ item }}_check" {% if saved_data.get(item, {}).get('check') %}checked{% endif %}> {{ item }}</label>
                <textarea name="{{ item }}_comment" placeholder="Comment..." rows="2" cols="80">{{ saved_data.get(item, {}).get('comment', '') }}</textarea>
                <br><br>
            {% endfor %}
            <br>
            <input type="submit" value="Save & Return">
        </form>
        <br><a href="/">Back to Dashboard</a>
    </body>
    </html>
    """, section=section, section_title=section_title, items=items, saved_data=saved_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)

@app.route('/export/csv')
def export_csv():
    import csv
    from io import StringIO
    responses = load_responses()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Item", "Checked", "Comment"])
    for section, secdata in checklist_data.items():
        section_responses = responses.get(section, {})
        for item in secdata["items"]:
            res = section_responses.get(item, {})
            writer.writerow([item, res.get("check", False), res.get("comment", "")])
    output.seek(0)
    return app.response_class(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=dnv_checklist.csv"}
    )

@app.route('/report')
def full_report():
    responses = load_responses()
    return render_template_string("""
    <html>
    <head>
        <title>Printable Checklist Report</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h2 { border-bottom: 1px solid #ccc; margin-top: 30px; }
            .check { color: green; }
            .uncheck { color: red; }
            textarea { width: 100%; max-width: 600px; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h1>DNV-ST-0145 Chapter 9 - Full Checklist Report</h1>
        <button onclick="window.print()">🖨 Print This Report</button>
        {% for section, secdata in checklist_data.items() %}
            <h2>{{ secdata["title"] }}</h2>
            <ul>
            {% for item in secdata["items"] %}
                {% set result = responses.get(section, {}).get(item, {}) %}
                <li>
                    <strong class="{{ 'check' if result.get('check') else 'uncheck' }}">
                        [{{ '✔' if result.get('check') else '✘' }}]
                    </strong>
                    {{ item }}
                    {% if result.get('comment') %}
                        <div><em>Comment:</em><br>{{ result.get('comment') }}</div>
                    {% endif %}
                </li>
            {% endfor %}
            </ul>
        {% endfor %}
        <br><button onclick="window.print()">🖨 Print This Report</button>
    </body>
    </html>
    """, checklist_data=checklist_data, responses=responses)
