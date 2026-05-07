# ☁ Cloud Monitoring Dashboard

A **professional, resume-worthy** Cloud Infrastructure Monitoring Dashboard built with **Python & Flask** — no Docker, no Kubernetes, no complex setup required.

---

## 📋 Features

| Feature | Description |
|---|---|
| **CPU Usage** | Real-time CPU percent, core count, frequency |
| **RAM Usage** | Used / Total / Available memory |
| **Disk Usage** | Storage used, free space, health status |
| **Server Health** | Overall health score (animated ring) |
| **Active Services** | 6 simulated microservices with status |
| **Deployment Status** | 4 environments (Prod / Staging / Dev / DR) |
| **Network I/O** | Total bytes sent & received |
| **System Info** | OS, hostname, Python version, uptime |
| **Auto-Refresh** | Dashboard updates every 10 seconds |
| **REST API** | `/api/metrics` returns JSON |

---

## 🚀 Quick Start

### 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### 2 — Run the app
```bash
python app.py
```

### 3 — Open in browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
cloud_monitoring_dashboard/
│
├── app.py                 ← Flask app + all system metrics logic
├── requirements.txt       ← Only 2 dependencies: flask + psutil
├── README.md              ← This file
│
└── templates/
    └── index.html         ← Dark-theme dashboard UI (Jinja2)
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Main dashboard page |
| `/api/metrics` | GET | Live metrics as JSON |
| `/api/health` | GET | Simple health check |

---

## 🛠 Technologies Used

- **Python 3.8+**
- **Flask 3.0** — Web framework
- **psutil 5.9** — System metrics library
- **Jinja2** — HTML templating (comes with Flask)
- **Vanilla CSS** — Dark theme, no external CSS framework

---

## 📌 Resume Description

> *Developed a real-time Cloud Infrastructure Monitoring Dashboard using Python (Flask + psutil) that displays live CPU, RAM, disk, and network metrics. Implemented a RESTful API endpoint for metric data and a professional dark-theme UI with auto-refresh capability, simulating a production cloud monitoring tool.*

---

## 👤 Author

Built as a Python / Cloud / DevOps learning project.
