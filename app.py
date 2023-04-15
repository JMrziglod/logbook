from pathlib import Path


from flask import Flask, render_template
import plotly
import plotly.express as px

app = Flask(__name__)

table = {}
widgets = [
    [
    """
fig = px.scatter(table["iris"], x="sepal_width", y="sepal_length", color="species")
html = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    """,
    """
fig = px.scatter(table["iris"], x="sepal_width", y="sepal_length", color="petal_length")
html = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    """,
    ]
]

@app.route("/")
def index():
    widgets_as_strings = []
    for r, row in enumerate(widgets):
        row_as_string = []
        for c, code in enumerate(row):
            locals = {}
            exec(code, globals(), locals)
            row_as_string.append({
                    "row": r,
                    "col": c,
                    "code": code,
                    "html": locals["html"]
                })
        widgets_as_strings.append(row_as_string)
    return render_template("dashboard.html", widgets=widgets_as_strings)

def run_file(filename):
    code = Path(filename).read_text()
    exec(code)

project = "projects/rabid"

run_file(f"{project}/tables.py")
app.run(debug=True)