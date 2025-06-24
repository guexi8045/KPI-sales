import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) 

from flask import Flask
from flask_cors import CORS
from backend.routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
