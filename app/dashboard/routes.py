from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import bp
from app.models import SystemMetric, User
from app import db
import psutil
from datetime import datetime


def collect_metrics():
    """Collect current system metrics and save to DB."""
    net = psutil.net_io_counters()
    metric = SystemMetric(
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage('/').percent,
        network_sent=net.bytes_sent,
        network_recv=net.bytes_recv,
    )
    db.session.add(metric)
    db.session.commit()
    return metric


@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    # Collect fresh snapshot
    metric = collect_metrics()

    # Last 20 historical metrics for charts
    history = SystemMetric.query.order_by(SystemMetric.timestamp.desc()).limit(20).all()
    history.reverse()

    # Summary stats
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    stats = {
        'cpu': cpu,
        'memory': mem.percent,
        'memory_used': round(mem.used / 1024 / 1024 / 1024, 2),
        'memory_total': round(mem.total / 1024 / 1024 / 1024, 2),
        'disk': disk.percent,
        'disk_used': round(disk.used / 1024 / 1024 / 1024, 2),
        'disk_total': round(disk.total / 1024 / 1024 / 1024, 2),
        'net_sent': round(net.bytes_sent / 1024 / 1024, 2),
        'net_recv': round(net.bytes_recv / 1024 / 1024, 2),
    }

    user_count = User.query.count()
    total_snapshots = SystemMetric.query.count()

    return render_template(
        'dashboard/index.html',
        stats=stats,
        history=history,
        user_count=user_count,
        total_snapshots=total_snapshots,
        now=datetime.utcnow()
    )
