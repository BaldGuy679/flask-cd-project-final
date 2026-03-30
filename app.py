from flask import Flask, render_template_string
from datetime import datetime
import socket
import os

app = Flask(__name__)

VERSION = "1.0"

# Ambil hostname & IP VPS
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

@app.route("/")
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CD Project - Bintang Samuel</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                text-align: center;
                padding: 50px;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                display: inline-block;
            }}
            h1 {{
                color: #2c3e50;
            }}
            p {{
                font-size: 18px;
                margin: 10px 0;
            }}
            .highlight {{
                color: #27ae60;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Continuous Deployment Project</h1>
            <p><strong>Nama:</strong> Bintang Samuel Samosir</p>
            <p><strong>Versi Aplikasi:</strong> <span class="highlight">{VERSION}</span></p>
            <p><strong>Waktu Deploy:</strong> {current_time}</p>
            <p><strong>Hostname Server:</strong> {hostname}</p>
            <p><strong>IP Server:</strong> {ip_address}</p>
            <hr>
            <p>✅ Deployment berhasil</p>
            <p>🔁 Update otomatis melalui GitHub Actions</p>
        </div>
    </body>
    </html>
    """
    return html


@app.route("/health")
def health():
    return {
        "status": "running",
        "version": VERSION,
        "timestamp": datetime.now()
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)