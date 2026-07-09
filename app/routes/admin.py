from functools import wraps

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Bill, LoginAttempt, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash("Admin access required.")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/all_users")
@login_required
@admin_required
def view_all_users():
    users = User.query.all()
    security_risks = (
        LoginAttempt.query.filter_by(user_id=None)
        .order_by(LoginAttempt.created_at.desc())
        .all()
    )
    return render_template(
        "all_users.html", users=users, security_risks=security_risks
    )


@admin_bp.route("/user/<int:user_id>/bills")
@login_required
@admin_required
def view_user_bills(user_id):
    user = User.query.get_or_404(user_id)
    bills = Bill.query.filter_by(creator_id=user_id).all()
    return render_template("user_paid_bills.html", user=user, bills=bills)


@admin_bp.route("/user/<int:user_id>/login_attempts")
@login_required
@admin_required
def view_user_login_attempts(user_id):
    user = User.query.get_or_404(user_id)
    user_login_attempts = (
        LoginAttempt.query.filter_by(user_id=user_id)
        .order_by(LoginAttempt.created_at.desc())
        .all()
    )
    return render_template(
        "user_login_attempts.html",
        user=user,
        user_login_attempts=user_login_attempts,
    )


@admin_bp.route("/delete_bill/<int:bill_id>")
@login_required
@admin_required
def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    db.session.delete(bill)
    db.session.commit()
    flash("Bill deleted successfully.")
    return redirect(url_for("admin.view_user_bills", user_id=bill.creator_id))


@admin_bp.route("/archive_bill/<int:bill_id>")
@login_required
@admin_required
def archive_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    bill.is_draft = True
    db.session.commit()
    flash("Bill archived successfully (moved to drafts).")
    return redirect(url_for("admin.view_user_bills", user_id=bill.creator_id))
