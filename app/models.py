from datetime import UTC, datetime

from flask_login import UserMixin

from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    paid_bills_created = db.relationship("Bill", backref="creator", lazy=True)
    paid_bills_shared = db.relationship("BillShare", backref="user", lazy=True)

    @property
    def unread_notifications(self):
        return [n for n in self.notifications if not n.is_read]

    @property
    def unread_notifications_count(self):
        return len(self.unread_notifications)


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    shares_paid_status = db.Column(db.String(20), default="pending")
    payment_image = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    shares = db.relationship(
        "BillShare", backref="bill", cascade="all, delete-orphan", lazy=True
    )
    shares_due_date = db.Column(db.DateTime, nullable=True)
    is_draft = db.Column(db.Boolean, default=True)


class BillShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    share_amount = db.Column(db.Float, nullable=False)
    share_paid = db.Column(db.Boolean, default=False)
    payment_image = db.Column(db.LargeBinary, nullable=True)

    @property
    def individual_status(self):
        now = datetime.now(UTC).replace(tzinfo=None)

        if self.share_paid and now > self.bill.shares_due_date:
            return "Late Payment"
        elif self.share_paid and now <= self.bill.shares_due_date:
            return "Paid on Time"
        elif now > self.bill.shares_due_date:
            return "Overdue"
        else:
            return "Due"


class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    email_attempted = db.Column(db.String(150), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    user = db.relationship("User", backref="notifications")
