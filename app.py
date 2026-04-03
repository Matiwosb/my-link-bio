from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# In-memory storage for links submitted through the homepage form.
links = [
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com"},
    {"name": "Personal Blog", "url": "https://example.com"},
]


@app.route("/")
def home():
    return render_template("index.html", links=links)


@app.route("/add", methods=["POST"])
def add_link():
    site_name = request.form.get("site_name", "").strip()
    site_url = request.form.get("site_url", "").strip()

    if site_name and site_url:
        links.append({"name": site_name, "url": site_url})

    return redirect(url_for("home"))


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    links = [
        {"name": "GitHub", "url": "https://github.com"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com"},
        {"name": "Personal Blog", "url": "https://example.com"},
    ]
    return render_template("index.html", links=links)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
