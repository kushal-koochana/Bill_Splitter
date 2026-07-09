import secrets
from datetime import UTC, datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import LoginAttempt, User
from app.utils import send_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = str(request.form.get("username")).strip()
        email = str(request.form.get("email")).lower().strip()
        password = str(request.form.get("password"))
        completed_fields = username and email and password

        if not completed_fields:
            flash("Please fill in all required fields.")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please use a unique email.")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash(
                "Username already taken. Please choose a different username."
            )
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username, email=email, password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Directing to login page to login...")
        return redirect(url_for("auth.login"))
    return render_template("registration.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = str(request.form.get("email")).lower().strip()
        password = str(request.form.get("password"))
        user = User.query.filter_by(email=email).first()
        is_correct_password = False

        if user:
            is_correct_password = check_password_hash(
                user.password_hash, password
            )

        if user and is_correct_password:
            login_user(user)
            flash("Login successful.")
            login_attempt = LoginAttempt(
                user_id=user.id, email_attempted=email, success=True
            )
            db.session.add(login_attempt)
            db.session.commit()
            return redirect(url_for("index"))

        login_attempt = LoginAttempt(
            user_id=user.id if user else None,
            email_attempted=email,
            success=False,
        )
        db.session.add(login_attempt)
        db.session.commit()

        if not user:
            flash("User does not exist.")
        elif not is_correct_password:
            flash("Incorrect password.")

        return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = str(request.form.get("email")).lower().strip()
        user = User.query.filter_by(email=email).first()

        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiry = datetime.now(UTC).replace(
                tzinfo=None
            ) + timedelta(hours=1)
            db.session.commit()
            reset_link = url_for(
                "auth.reset_password", token=token, _external=True
            )
            msg = (
                f"Hello {user.username},\n"
                "Did you request a password reset? Click the link below to "
                "reset your password (otherwise ignore it, if it wasn't you): "
                f"\n{reset_link}\n"
                "This link expires in 1 hour.\n"
                "From admin"
            )
            send_email(
                subject="Password Reset Request",
                recipient=user.email,
                email_body=msg,
            )

        flash("If the email exists, a reset link has been sent.")
        return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    now = datetime.now(UTC).replace(tzinfo=None)

    if (
        not user
        or not user.reset_token_expiry
        or user.reset_token_expiry < now
    ):
        flash("Reset link is invalid or expired.")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        new_password = str(request.form.get("password"))
        if not new_password:
            flash("Password cannot be empty.")
            return redirect(request.url)
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        flash("Password reset successful. Please login.")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out...")
    return redirect(url_for("auth.login"))
