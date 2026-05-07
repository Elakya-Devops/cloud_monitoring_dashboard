"""
=============================================================
  Cloud Infrastructure Monitoring Dashboard
  Author  : Python / Cloud / DevOps Project
  Version : 1.0
  Run     : python app.py
=============================================================
"""

import os
import random
import datetime
import platform

import psutil                   # System metrics (CPU, RAM, Disk, Network)
from flask import Flask, render_template, jsonify

# ── Flask app setup ──────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "cloud_monitor_secret_2024"

# ── Helper utilities ─────────────────────────────────────────

def get_size(bytes_value, suffix="B"):
    """Convert raw bytes into a human-readable string (KB / MB / GB)."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_value < factor:
            return f"{bytes_value:.2f} {unit}{suffix}"
        bytes_value /= factor


def health_label(value: float) -> str:
    """Return a health label based on a percentage value."""
    if value < 60:
        return "Healthy"
    elif value < 85:
        return "Warning"
    else:
        return "Critical"


def health_color(value: float) -> str:
    """Return a CSS color class based on a percentage value."""
    if value < 60:
        return "green"
    elif value < 85:
        return "yellow"
    else:
        return "red"


# ── Real-time system metrics ─────────────────────────────────

def collect_metrics():
    """
    Gather live system metrics using the psutil library.
    Returns a dict that will be passed directly to the Jinja template.
    """

    # ── CPU ──────────────────────────────────────────────────
    cpu_percent      = psutil.cpu_percent(interval=0.5)
    cpu_count_logic  = psutil.cpu_count(logical=True)
    cpu_count_phys   = psutil.cpu_count(logical=False)
    cpu_freq         = psutil.cpu_freq()
    cpu_freq_cur     = round(cpu_freq.current, 1) if cpu_freq else 0

    # ── RAM ──────────────────────────────────────────────────
    ram              = psutil.virtual_memory()
    ram_percent      = ram.percent
    ram_total        = get_size(ram.total)
    ram_used         = get_size(ram.used)
    ram_available    = get_size(ram.available)

    # ── Disk ─────────────────────────────────────────────────
    disk             = psutil.disk_usage("/")
    disk_percent     = disk.percent
    disk_total       = get_size(disk.total)
    disk_used        = get_size(disk.used)
    disk_free        = get_size(disk.free)

    # ── Network ──────────────────────────────────────────────
    net              = psutil.net_io_counters()
    net_sent         = get_size(net.bytes_sent)
    net_recv         = get_size(net.bytes_recv)

    # ── System info ──────────────────────────────────────────
    boot_time        = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime_delta     = datetime.datetime.now() - boot_time
    uptime_hours     = int(uptime_delta.total_seconds() // 3600)
    uptime_minutes   = int((uptime_delta.total_seconds() % 3600) // 60)
    uptime_str       = f"{uptime_hours}h {uptime_minutes}m"

    system_info = {
        "os"      : platform.system(),
        "version" : platform.version()[:40],   # trim long strings
        "node"    : platform.node(),
        "arch"    : platform.machine(),
        "python"  : platform.python_version(),
    }

    # ── Simulated cloud / deployment data ────────────────────
    # (In a real cloud setup these would come from cloud SDK calls)
    services = [
        {"name": "Web Server",      "status": "Running",  "port": 8080, "uptime": "12h 34m"},
        {"name": "Database",        "status": "Running",  "port": 5432, "uptime": "5d 3h"},
        {"name": "Cache (Redis)",   "status": "Running",  "port": 6379, "uptime": "2d 11h"},
        {"name": "Message Queue",   "status": "Warning",  "port": 5672, "uptime": "18h 22m"},
        {"name": "Auth Service",    "status": "Running",  "port": 3000, "uptime": "4d 7h"},
        {"name": "Monitoring Agent","status": "Running",  "port": 9090, "uptime": "6h 10m"},
    ]

    deployments = [
        {"env": "Production",  "version": "v2.4.1", "status": "Live",      "deployed": "2 hours ago",   "health": 98},
        {"env": "Staging",     "version": "v2.5.0", "status": "Testing",   "deployed": "30 mins ago",   "health": 87},
        {"env": "Development", "version": "v2.5.1", "status": "Building",  "deployed": "5 mins ago",    "health": 65},
        {"env": "DR Region",   "version": "v2.4.1", "status": "Standby",   "deployed": "1 day ago",     "health": 100},
    ]

    # Overall server health — average of CPU + RAM + Disk
    overall_health = round(100 - (cpu_percent + ram_percent + disk_percent) / 3, 1)
    overall_health = max(0, min(100, overall_health))   # clamp 0-100

    return {
        # ── CPU
        "cpu_percent"    : cpu_percent,
        "cpu_health"     : health_label(cpu_percent),
        "cpu_color"      : health_color(cpu_percent),
        "cpu_cores_logic": cpu_count_logic,
        "cpu_cores_phys" : cpu_count_phys,
        "cpu_freq"       : cpu_freq_cur,

        # ── RAM
        "ram_percent"    : ram_percent,
        "ram_health"     : health_label(ram_percent),
        "ram_color"      : health_color(ram_percent),
        "ram_total"      : ram_total,
        "ram_used"       : ram_used,
        "ram_available"  : ram_available,

        # ── Disk
        "disk_percent"   : disk_percent,
        "disk_health"    : health_label(disk_percent),
        "disk_color"     : health_color(disk_percent),
        "disk_total"     : disk_total,
        "disk_used"      : disk_used,
        "disk_free"      : disk_free,

        # ── Network
        "net_sent"       : net_sent,
        "net_recv"       : net_recv,

        # ── System
        "uptime"         : uptime_str,
        "system_info"    : system_info,
        "overall_health" : overall_health,
        "health_label"   : health_label(100 - overall_health),

        # ── Cloud / Services
        "services"       : services,
        "deployments"    : deployments,

        # ── Timestamp
        "last_updated"   : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """
    Main dashboard route — renders the full monitoring page.
    All metrics are fetched fresh on every page load.
    """
    metrics = collect_metrics()
    return render_template("index.html", **metrics)


@app.route("/api/metrics")
def api_metrics():
    """
    JSON endpoint used by the front-end auto-refresh (AJAX).
    Returns live metrics every time it is called.
    """
    metrics = collect_metrics()
    return jsonify(metrics)


@app.route("/api/health")
def api_health():
    """Simple health-check endpoint — useful for uptime monitors."""
    return jsonify({
        "status"  : "ok",
        "service" : "cloud-monitoring-dashboard",
        "time"    : datetime.datetime.now().isoformat(),
    })


# ── Entry point ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  ☁  Cloud Infrastructure Monitoring Dashboard")
    print("=" * 55)
    print(f"  → Open your browser at: http://127.0.0.1:5000")
    print(f"  → Press CTRL+C to stop the server")
    print("=" * 55)
    # debug=True enables auto-reload during development
    app.run(debug=False, host="0.0.0.0", port=5000)
