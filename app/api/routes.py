from flask import jsonify
from flask_login import login_required
from app.api import bp
from app.models import SystemMetric
from app.dashboard.routes import collect_metrics
import psutil


@bp.route('/metrics/latest')
@login_required
def metrics_latest():
    """Return latest system metrics snapshot."""
    metric = collect_metrics()
    return jsonify({'status': 'ok', 'data': metric.to_dict()})


@bp.route('/metrics/history')
@login_required
def metrics_history():
    """Return last 50 stored metric snapshots."""
    records = SystemMetric.query.order_by(SystemMetric.timestamp.desc()).limit(50).all()
    records.reverse()
    return jsonify({'status': 'ok', 'count': len(records), 'data': [r.to_dict() for r in records]})


@bp.route('/metrics/live')
@login_required
def metrics_live():
    """Return current live system stats (no DB write)."""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    return jsonify({
        'status': 'ok',
        'data': {
            'cpu_percent': cpu,
            'memory_percent': mem.percent,
            'disk_percent': disk.percent,
            'network_sent_mb': round(net.bytes_sent / 1024 / 1024, 2),
            'network_recv_mb': round(net.bytes_recv / 1024 / 1024, 2),
        }
    })


@bp.route('/health')
def health():
    """Health check endpoint for deployment verification."""
    return jsonify({'status': 'healthy', 'message': 'Flask CD Dashboard is running'})
