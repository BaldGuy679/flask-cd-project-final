from flask import Flask
from datetime import datetime

app = Flask(__name__)

VERSION = "1.0"

@app.route("/")
def home():
    return f"""
    <h1>Continuous Deployment Project</h1>
    <p>Nama: Bintang Samuel Samosir</p>
    <p>Version: {VERSION}</p>
    <p>Deploy Time: {datetime.now()}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
