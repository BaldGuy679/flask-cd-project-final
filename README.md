# SysWatch — Flask CD Dashboard

Proyek Tugas Akhir: **Implementasi Continuous Deployment Aplikasi Web Menggunakan GitHub Actions pada Infrastruktur VPS**

Program Studi Teknologi Rekayasa Internet — Universitas Gadjah Mada

---

## 📋 Deskripsi Proyek

SysWatch adalah aplikasi web monitoring sistem berbasis Flask yang dilengkapi dengan pipeline **Continuous Deployment** otomatis menggunakan GitHub Actions. Setiap push ke branch `main` akan memicu pipeline CI/CD yang menjalankan unit test dan secara otomatis men-deploy aplikasi ke VPS.

---

## 🏗️ Struktur Proyek

```
flask-cd-project/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── models.py            # SQLAlchemy models (User, SystemMetric)
│   ├── auth/
│   │   ├── __init__.py      # Auth blueprint
│   │   └── routes.py        # Login, register, logout
│   ├── dashboard/
│   │   ├── __init__.py      # Dashboard blueprint
│   │   └── routes.py        # Dashboard & metrics collection
│   ├── api/
│   │   ├── __init__.py      # API blueprint
│   │   └── routes.py        # REST API endpoints
│   ├── templates/
│   │   ├── base.html        # Base layout
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── dashboard/
│   │       └── index.html
│   └── static/
├── tests/
│   ├── conftest.py
│   └── test_app.py          # Unit tests (model, auth, api, dashboard)
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions CI/CD pipeline
├── config.py                # Config & TestingConfig
├── run.py                   # App entrypoint
├── requirements.txt
├── pytest.ini
├── flask-cd-project.service # Systemd service file
├── .env.example
└── .gitignore
```

---

## ⚙️ Cara Menjalankan Lokal

### 1. Clone & setup environment
```bash
git clone https://github.com/<username>/flask-cd-project.git
cd flask-cd-project
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
```bash
cp .env.example .env
# Edit .env sesuai kebutuhan
```

### 4. Jalankan aplikasi
```bash
python run.py
```
Buka browser: `http://localhost:5000`

---

## 🧪 Menjalankan Unit Test

```bash
# Jalankan semua test
pytest

# Dengan coverage report
pytest --cov=app --cov-report=term-missing

# Output HTML coverage
pytest --cov=app --cov-report=html
```

---

## 🌐 REST API Endpoints

| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| GET | `/api/health` | ❌ | Health check deployment |
| GET | `/api/metrics/live` | ✅ | Snapshot metrik sistem real-time |
| GET | `/api/metrics/latest` | ✅ | Snapshot terbaru dari database |
| GET | `/api/metrics/history` | ✅ | 50 snapshot terakhir |

---

## 🚀 Deployment ke VPS

### Persiapan VPS (Ubuntu 22.04)

```bash
# Install dependencies
sudo apt update && sudo apt install python3-pip python3-venv nginx git -y

# Clone repo
sudo mkdir -p /var/www/flask-cd-project
sudo git clone https://github.com/<username>/flask-cd-project.git /var/www/flask-cd-project

# Setup virtualenv
cd /var/www/flask-cd-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup log directory
sudo mkdir -p /var/log/flask-cd-project
sudo chown www-data:www-data /var/log/flask-cd-project

# Setup systemd service
sudo cp flask-cd-project.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable flask-cd-project
sudo systemctl start flask-cd-project
```

### GitHub Actions Secrets

Tambahkan secrets berikut di repo GitHub (`Settings > Secrets`):

| Secret | Deskripsi |
|--------|-----------|
| `VPS_HOST` | IP address VPS |
| `VPS_USER` | Username SSH (misal: `ubuntu`) |
| `VPS_SSH_KEY` | Private key SSH |
| `VPS_PORT` | Port SSH (default: 22) |

### Alur CI/CD Pipeline

```
Push ke main
    │
    ▼
[GitHub Actions Trigger]
    │
    ├─► Job: test
    │       ├── Checkout code
    │       ├── Setup Python 3.11
    │       ├── pip install -r requirements.txt
    │       └── pytest --cov (jika GAGAL → pipeline berhenti)
    │
    └─► Job: deploy (hanya jika test LULUS)
            ├── SSH ke VPS
            ├── git pull origin main
            ├── pip install (update deps)
            ├── flask db upgrade
            ├── systemctl restart
            ├── Health check /api/health
            └── Catat deployment duration (ms)
```

---

## 📊 Fitur Monitoring

- **CPU Usage** — Persentase penggunaan processor real-time
- **Memory Usage** — RAM terpakai vs total
- **Disk Usage** — Kapasitas penyimpanan
- **Network I/O** — Total bytes sent/received
- **Historical Charts** — Grafik 20 snapshot terakhir (Chart.js)
- **Database logging** — Setiap kunjungan dashboard menyimpan snapshot ke SQLite

---

## 🛠️ Teknologi

| Layer | Teknologi |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite + SQLAlchemy ORM |
| Auth | Flask-Login + Werkzeug password hashing |
| Monitoring | psutil |
| Frontend | HTML/CSS/JS vanilla + Chart.js |
| Testing | pytest + pytest-cov |
| Server | Gunicorn |
| CI/CD | GitHub Actions |
| Deployment | VPS Ubuntu + systemd |

---

## 👤 Author

**[Nama Mahasiswa]**  
NIM: [NIM]  
Program Studi Teknologi Rekayasa Internet  
Universitas Gadjah Mada  
Tahun: 2025
