from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from backend.routes import register_routes

app = Flask(__name__, static_folder="frontend_build", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}})

register_routes(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
