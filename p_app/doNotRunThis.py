from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)


def generate_images():
    links = []

    for _ in range(10):
        response = requests.get(
            "https://api.waifu.im/images?IsNsfw=True",
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        # Change this according to the JSON returned by your API
        links.append(data["items"][0]["url"])

    return links


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/images")
def get_images():
    try:
        images = generate_images()
        return jsonify({"images": images})

    except requests.RequestException as error:
        return jsonify({
            "error": "Failed to fetch images",
            "details": str(error)
        }), 500

    except (KeyError, IndexError, TypeError) as error:
        return jsonify({
            "error": "Unexpected API response format",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
