from flask import Flask, flash, render_template
from flask_login import current_user, login_required

from app.config import Config
from app.extensions import db, login_manager, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.bills import bills_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(bills_bp)
    app.register_blueprint(admin_bp)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/help_and_credits")
    @login_required
    def help_and_credits():
        if not current_user.is_admin:
            return render_template("help_and_credits.html")
        flash("This is user guide, able to view in src.")
        return render_template("index.html")

    @app.route("/notifications/read", methods=["POST"])
    @login_required
    def mark_notifications_read():
        for notification in current_user.notifications:
            notification.is_read = True

        db.session.commit()
        return "", 204

    @app.cli.command("init-db")
    def init_db():
        """Clear existing data and create new tables."""
        from werkzeug.security import generate_password_hash

        from app.extensions import db
        from app.models import User

        db.create_all()

        admin_user = User.query.filter_by(email="admin@example.com").first()
        if not admin_user:
            admin_user = User(
                username="Admin",
                email="admin@example.com",
                password_hash=generate_password_hash("Password123"),
                is_admin=True,
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Database initialized and admin user created.")

    return app
