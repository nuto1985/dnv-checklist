from flask import Flask, render_template, request, redirect, url_for
import json, os
app = Flask(__name__)
@app.route("/section/<section_id>", methods=["GET", "POST"])
def section(section_id):
 with open("checklist_data.json") as f: checklist = json.load(f)
 with open("chapter_texts.json") as f: texts = json.load(f)
 section = checklist.get(section_id); states = [False]*len(section["items"]); comments = ["" for _ in section["items"]]
 if section is None: return "Not found", 404
 if request.method == "POST":
  states = [f"item_{i}" in request.form for i in range(len(section["items"]))]
  comments = [request.form.get(f"comment_{i}","") for i in range(len(section["items"]))]
 return render_template("section.html", title=f"Section {section_id} – {section['title']}", content=texts.get(section_id,""), items=section["items"], states=states, comments=comments)
@app.route("/") 
def index(): return redirect(url_for("section", section_id="9.1"))
if __name__ == "__main__":
 port = int(os.environ.get("PORT", 5000)); app.run(host="0.0.0.0", port=port)