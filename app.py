from pathlib import Path


from flask import Flask, render_template, request
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
            row_as_string.append(render_widget(r, c, code))
        widgets_as_strings.append(row_as_string)
    return render_template("dashboard.html", widgets=widgets_as_strings)

def render_widget(row, col, code):
    l = {}
    print(code)
    try:
        exec(code, globals(), l)
    except Exception as err: 
        l["html"] = f"&#9888;<b>ERROR:</b> {err}"
    return {
                    "row": row,
                    "col": col,
                    "code": code,
                    "html": l["html"],
                }

@app.route("/widget/edit/<int:row>/<int:col>", methods=['GET', "POST"])
def edit_widget(row, col):
    content = request.json
    widgets[row][col] = content['code']
    return render_widget(row, col, content['code'])

def run_file(filename):
    code = Path(filename).read_text()
    exec(code)

project = "projects/rabid"

run_file(f"{project}/tables.py")
app.run(debug=True)