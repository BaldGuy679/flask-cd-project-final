import pytest
from app import create_app, db
from app.models import User, SystemMetric
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_user(app):
    """Create and return a test user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


# ─── MODEL TESTS ───────────────────────────────────────────────────────────────

class TestUserModel:
    def test_password_hashing(self, app):
        with app.app_context():
            u = User(username='alice', email='alice@test.com')
            u.set_password('secret123')
            assert u.password_hash != 'secret123'
            assert u.check_password('secret123')
            assert not u.check_password('wrongpass')

    def test_user_repr(self, app):
        with app.app_context():
            u = User(username='bob', email='bob@test.com')
            assert 'bob' in repr(u)

    def test_user_defaults(self, app):
        with app.app_context():
            u = User(username='charlie', email='charlie@test.com')
            u.set_password('pass')
            db.session.add(u)
            db.session.commit()
            assert u.is_admin is False
            assert u.created_at is not None


class TestSystemMetricModel:
    def test_metric_to_dict(self, app):
        with app.app_context():
            m = SystemMetric(
                cpu_percent=45.5,
                memory_percent=60.0,
                disk_percent=30.0,
                network_sent=1024 * 1024 * 100,
                network_recv=1024 * 1024 * 50,
            )
            db.session.add(m)
            db.session.commit()
            d = m.to_dict()
            assert d['cpu_percent'] == 45.5
            assert d['memory_percent'] == 60.0
            assert 'timestamp' in d
            assert d['network_sent'] == 100.0


# ─── AUTH TESTS ────────────────────────────────────────────────────────────────

class TestAuthRoutes:
    def test_login_page_loads(self, client):
        r = client.get('/auth/login')
        assert r.status_code == 200
        assert b'login' in r.data.lower()

    def test_register_page_loads(self, client):
        r = client.get('/auth/register')
        assert r.status_code == 200

    def test_register_user(self, client, app):
        r = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123',
        }, follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            assert user is not None

    def test_register_first_user_is_admin(self, client, app):
        client.post('/auth/register', data={
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'confirm_password': 'admin123',
        })
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            assert user.is_admin is True

    def test_register_password_mismatch(self, client):
        r = client.post('/auth/register', data={
            'username': 'x',
            'email': 'x@x.com',
            'password': 'pass1',
            'confirm_password': 'pass2',
        }, follow_redirects=True)
        assert b'do not match' in r.data.lower()

    def test_login_valid(self, client, auth_user, app):
        with app.app_context():
            r = client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password123',
            }, follow_redirects=True)
            assert r.status_code == 200

    def test_login_invalid(self, client, auth_user, app):
        with app.app_context():
            r = client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'wrongpass',
            }, follow_redirects=True)
            assert b'invalid' in r.data.lower()

    def test_duplicate_username(self, client, auth_user, app):
        with app.app_context():
            r = client.post('/auth/register', data={
                'username': 'testuser',
                'email': 'other@example.com',
                'password': 'pass123',
                'confirm_password': 'pass123',
            }, follow_redirects=True)
            assert b'already taken' in r.data.lower()


# ─── API TESTS ─────────────────────────────────────────────────────────────────

class TestApiRoutes:
    def test_health_endpoint(self, client):
        r = client.get('/api/health')
        assert r.status_code == 200
        data = r.get_json()
        assert data['status'] == 'healthy'

    def test_metrics_latest_requires_auth(self, client):
        r = client.get('/api/metrics/latest')
        assert r.status_code == 302  # redirect to login

    def test_metrics_live_requires_auth(self, client):
        r = client.get('/api/metrics/live')
        assert r.status_code == 302

    def test_metrics_history_requires_auth(self, client):
        r = client.get('/api/metrics/history')
        assert r.status_code == 302


# ─── DASHBOARD TESTS ───────────────────────────────────────────────────────────

class TestDashboardRoutes:
    def test_dashboard_requires_auth(self, client):
        r = client.get('/')
        assert r.status_code == 302
        assert '/auth/login' in r.headers['Location']
