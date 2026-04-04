from flask import Flask, redirect, render_template, request, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


# Shared fallback text for missing page metadata.
NOT_AVAILABLE = "Not Available"


def extract_link_metadata(site_url):
    """Fetch a URL and extract Open Graph title/description/image metadata."""
    metadata = {
        "title": NOT_AVAILABLE,
        "description": NOT_AVAILABLE,
        "image_url": NOT_AVAILABLE,
    }

    try:
        response = requests.get(site_url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Pull Open Graph values and keep defaults if tags are missing.
        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")

        if og_title and og_title.get("content"):
            metadata["title"] = og_title["content"].strip()
        if og_description and og_description.get("content"):
            metadata["description"] = og_description["content"].strip()
        if og_image and og_image.get("content"):
            metadata["image_url"] = og_image["content"].strip()
    except requests.RequestException:
        # Keep fallback metadata values when fetch fails.
        pass

    return metadata


# In-memory storage for links submitted through the homepage form.
links = [
    {
        "name": "GitHub",
        "url": "https://github.com",
        "title": NOT_AVAILABLE,
        "description": NOT_AVAILABLE,
        "image_url": NOT_AVAILABLE,
    },
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com",
        "title": NOT_AVAILABLE,
        "description": NOT_AVAILABLE,
        "image_url": NOT_AVAILABLE,
    },
    {
        "name": "Personal Blog",
        "url": "https://example.com",
        "title": NOT_AVAILABLE,
        "description": NOT_AVAILABLE,
        "image_url": NOT_AVAILABLE,
    },
]


@app.route("/")
def home():
    return render_template("index.html", links=links)


@app.route("/add", methods=["POST"])
def add_link():
    site_name = request.form.get("site_name", "").strip()
    site_url = request.form.get("site_url", "").strip()

    if site_name and site_url:
        metadata = extract_link_metadata(site_url)
        links.append(
            {
                "name": site_name,
                "url": site_url,
                "title": metadata["title"],
                "description": metadata["description"],
                "image_url": metadata["image_url"],
            }
        )

    return redirect(url_for("home"))


@app.route("/edit/<int:link_index>", methods=["GET", "POST"])
def edit_link(link_index):
    if not 0 <= link_index < len(links):
        return redirect(url_for("home"))

    if request.method == "POST":
        site_name = request.form.get("site_name", "").strip()
        site_url = request.form.get("site_url", "").strip()

        if site_name and site_url:
            metadata = extract_link_metadata(site_url)
            links[link_index] = {
                "name": site_name,
                "url": site_url,
                "title": metadata["title"],
                "description": metadata["description"],
                "image_url": metadata["image_url"],
            }

        return redirect(url_for("home"))

    return render_template("edit.html", link=links[link_index], link_index=link_index)


@app.route("/delete/<int:link_index>", methods=["POST"])
def delete_link(link_index):
    if 0 <= link_index < len(links):
        links.pop(link_index)

    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
