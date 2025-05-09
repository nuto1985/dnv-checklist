
from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
CHECKLIST_FILE = "checklist_data.json"
TEXT_FILE = "chapter_texts.json"

def load_data():
    with open(CHECKLIST_FILE) as f:
        checklist = json.load(f)
    with open(TEXT_FILE) as f:
        texts = json.load(f)
    return checklist, texts

@app.route("/")
def index():
    checklist, _ = load_data()
    section_ids = sorted(checklist.keys())
    return redirect(url_for("section", section_id=section_ids[0]))

@app.route("/section/<section_id>", methods=["GET", "POST"])
def section(section_id):
    checklist, texts = load_data()
    section = checklist.get(section_id)
    if not section:
        return "Section not found", 404
    states = [False] * len(section["items"])
    comments = [""] * len(section["items"])
    if request.method == "POST":
        states = [f"item_{i}" in request.form for i in range(len(section["items"]))]
        comments = [request.form.get(f"comment_{i}", "") for i in range(len(section["items"]))]
    section_ids = sorted(checklist.keys())
    return render_template("section.html", title=f"{section_id} – {section['title']}",
        content=texts.get(section_id, ""), items=section["items"],
        states=states, comments=comments, section_ids=section_ids)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
