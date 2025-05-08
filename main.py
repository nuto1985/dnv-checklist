from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

with open("checklist_data_with_requirements.json", "r") as f:
    checklist_data = json.load(f)

RESPONSES_FILE = "responses.json"
if not os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, "w") as f:
        json.dump({}, f)

def load_responses():
    with open(RESPONSES_FILE, "r") as f:
        return json.load(f)

def save_responses(responses):
    with open(RESPONSES_FILE, "w") as f:
        json.dump(responses, f)

@app.route("/")
def index():
    responses = load_responses()
    progress = {
        sec: sum(1 for item in responses.get(sec, []) if item.get("checked"))
        for sec in checklist_data
    }
    counts = {sec: len(data["items"]) for sec, data in checklist_data.items()}
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>DNV Checklist Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .section { margin-bottom: 15px; }
        .completed { color: green; }
    </style>
</head>
<body>
    <h1>DNV-ST-0145 Chapter 9 Checklist</h1>
    <p>Click a section to fill out the checklist and view its requirements.</p>
    <ul>
        {% for sec, data in checklist_data.items() %}
        <li class="section">
            <a href="{{ url_for('section', section=sec) }}">{{ data['title'] }}</a>
            -
            {% set pc = progress.get(sec, 0) %}
            {% set total = counts[sec] %}
            {% if pc == total %}
            <span class="completed">Complete ({{ pc }}/{{ total }})</span>
            {% else %}
            In Progress ({{ pc }}/{{ total }})
            {% endif %}
        </li>
        {% endfor %}
    </ul>

    <a href="{{ url_for('report') }}">🧾 Print/Export Report</a>

    <!-- Chatbot UI -->
    <div id="chat-icon" style="position:fixed; bottom:20px; right:20px; background:#007BFF; color:white; padding:10px; border-radius:50%; cursor:pointer; z-index:1000;">💬</div>
    <div id="chat-box" style="display:none; position:fixed; bottom:70px; right:20px; width:300px; background:white; border:1px solid #ccc; padding:10px; box-shadow:0 0 10px rgba(0,0,0,0.2); z-index:1000;">
        <div id="chat-log" style="height:200px; overflow-y:auto; border-bottom:1px solid #ddd; margin-bottom:10px;"></div>
        <input id="chat-input" type="text" placeholder="Ask me something..." style="width:100%; padding:5px;">
    </div>
    <script src="{{ url_for('static', filename='chatbot.js') }}"></script>
</body>
</html>
""", checklist_data=checklist_data, progress=progress, counts=counts)

@app.route("/checklist/<section>", methods=["GET", "POST"])
def section(section):
    if section not in checklist_data:
        return "Section not found", 404

    responses = load_responses()
    section_data = checklist_data[section]
    user_data = responses.get(section, [{"checked": False, "comment": ""} for _ in section_data["items"]])

    if request.method == "POST":
        for i, item in enumerate(section_data["items"]):
            user_data[i]["checked"] = bool(request.form.get(f"item_{i}"))
            user_data[i]["comment"] = request.form.get(f"comment_{i}", "")
        responses[section] = user_data
        save_responses(responses)
        return redirect(url_for("index"))

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h2>{{ title }}</h2>
    <p><strong>Requirements:</strong><br>{{ requirements }}</p>
    <form method="post">
        {% for item, r in data %}
        <div>
            <label>
                <input type="checkbox" name="item_{{ loop.index0 }}" {% if r.checked %}checked{% endif %}>
                {{ item }}
            </label><br>
            <textarea name="comment_{{ loop.index0 }}" placeholder="Comment..." rows="2" cols="60">{{ r.comment }}</textarea>
        </div><br>
        {% endfor %}
        <button type="submit">Save</button>
    </form>
    <p><a href="{{ url_for('index') }}">⬅ Back to Dashboard</a></p>
</body>
</html>
""", title=section_data["title"], requirements=section_data.get("requirements", ""), data=zip(section_data["items"], user_data))

@app.route("/report")
def report():
    responses = load_responses()
    report_data = {}
    for sec, items in checklist_data.items():
        user_data = responses.get(sec, [{"checked": False, "comment": ""} for _ in items["items"]])
        report_data[sec] = {
            "title": items["title"],
            "items": [
                {
                    "text": text,
                    "checked": response["checked"],
                    "comment": response["comment"]
                } for text, response in zip(items["items"], user_data)
            ]
        }
    return jsonify(report_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)