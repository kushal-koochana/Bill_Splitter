import io
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Bill, BillShare, Notification, User
from app.utils import send_email

bills_bp = Blueprint("bills", __name__, url_prefix="/bills")


@bills_bp.route("/bills_dashboard")
@login_required
def bills_dashboard():
    drafted_bills = [
        bill for bill in current_user.paid_bills_created if bill.is_draft
    ]
    created_bills = [
        bill for bill in current_user.paid_bills_created if not bill.is_draft
    ]
    shared_bills = [
        share
        for share in current_user.paid_bills_shared
        if not share.bill.is_draft
    ]
    return render_template(
        "bills_dashboard.html",
        drafted_bills=drafted_bills,
        created_bills=created_bills,
        shared_bills=shared_bills,
    )


@bills_bp.route("/create_paid_bill", methods=["GET", "POST"])
@login_required
def create_paid_bill():
    if request.method == "POST":
        selected_user_ids = request.form.getlist("shared_persons")

        if not selected_user_ids:
            flash("You must select at least one user to share the bill with.")
            return redirect(url_for("bills.create_paid_bill"))

        title = str(request.form.get("title")).strip()
        amount = float(request.form.get("amount"))
        category = str(request.form.get("category"))
        shares_due_date_str = str(request.form.get("shares_due_date"))
        image_file = request.files.get("payment_image")
        are_fields_filled = all(
            [title, amount, category, shares_due_date_str, image_file]
        )

        if not are_fields_filled:
            flash("Please fill in all required fields.")
            return redirect(url_for("bills.create_paid_bill"))

        shares_due_date = datetime.strptime(shares_due_date_str, "%Y-%m-%d")
        new_bill = Bill(
            title=title,
            amount=amount,
            category=category,
            creator_id=current_user.id,
            payment_image=image_file.read(),
            shares_due_date=shares_due_date,
            is_draft=True,
        )
        db.session.add(new_bill)
        db.session.commit()
        selected_users = [int(uid) for uid in selected_user_ids]
        share_amount = float(amount) / (len(selected_users) + 1)

        for user_id in selected_users:
            share = BillShare(
                bill=new_bill, user_id=user_id, share_amount=share_amount
            )
            db.session.add(share)

        db.session.commit()
        flash("Bill draft saved!")
        return redirect(url_for("bills.bills_dashboard"))
    categories = ["Utilities", "Rent", "Groceries", "Entertainment", "Other"]
    users = User.query.filter(User.id != current_user.id).all()
    return render_template(
        "paid_bill_form.html",
        categories=categories,
        users=users,
        shared_user_ids=[],
    )


@bills_bp.route("/edit_paid_bill/<int:bill_id>", methods=["GET", "POST"])
@login_required
def edit_paid_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)

    if bill.creator_id != current_user.id:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    if not bill.is_draft:
        flash("Only draft bills can be edited")
        return redirect(url_for("bills.bills_dashboard"))

    if request.method == "POST":
        selected_user_ids = request.form.getlist("shared_persons")

        if not selected_user_ids:
            flash("You must select at least one user to share the bill with.")
            return redirect(url_for("bills.edit_paid_bill", bill_id=bill.id))

        title = str(request.form.get("title"))
        amount = float(request.form.get("amount"))
        category = str(request.form.get("category"))
        shares_due_date_str = str(request.form.get("shares_due_date"))
        shares_due_date = datetime.strptime(shares_due_date_str, "%Y-%m-%d")
        new_image = request.files.get("payment_image")
        are_fields_filled = all([title, amount, category, shares_due_date])

        if not are_fields_filled:
            flash("Please fill in all required fields.")
            return redirect(url_for("bills.edit_paid_bill", bill_id=bill.id))

        bill.title = title
        bill.amount = amount
        bill.category = category
        bill.shares_due_date = shares_due_date

        if new_image:
            bill.payment_image = new_image.read()

        selected_user_ids = request.form.getlist("shared_persons")
        BillShare.query.filter_by(bill_id=bill.id).delete()
        share_amount = bill.amount / (len(selected_user_ids) + 1)

        for uid in selected_user_ids:
            share = BillShare(
                bill=bill, user_id=int(uid), share_amount=share_amount
            )
            db.session.add(share)

        db.session.commit()
        flash("Bill draft updated!")
        return redirect(url_for("bills.bills_dashboard"))

    categories = ["Utilities", "Rent", "Groceries", "Entertainment", "Other"]
    users = User.query.filter(User.id != current_user.id).all()
    shared_user_ids = [share.user_id for share in bill.shares]
    return render_template(
        "paid_bill_form.html",
        bill=bill,
        categories=categories,
        users=users,
        shared_user_ids=shared_user_ids,
    )


@bills_bp.route("/send_paid_bill/<int:bill_id>")
@login_required
def send_paid_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)

    if bill.creator_id != current_user.id:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    if not bill.shares:
        flash("You must assign at least one user before sending.")
        return redirect(url_for("bills.bills_dashboard"))

    bill.is_draft = False
    bill.shares_paid_status = "pending"
    db.session.commit()

    for share in bill.shares:
        message = (
            f"{current_user.username} sent you a bill for "
            f"£{share.share_amount:.2f}"
        )
        notification = Notification(user_id=share.user_id, message=message)
        db.session.add(notification)
        send_email(
            subject="New Bill Assigned",
            recipient=share.user.email,
            email_body=message,
        )

    db.session.commit()
    flash("Bill sent successfully!")
    return redirect(url_for("bills.bills_dashboard"))


@bills_bp.route("/pay_share/<int:share_id>", methods=["GET", "POST"])
@login_required
def pay_share(share_id):
    share = BillShare.query.get_or_404(share_id)

    if share.user_id != current_user.id:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    if request.method == "POST":
        payment_image = request.files.get("payment_image")

        if not payment_image:
            flash("Please upload an image of the payment receipt.")
            return redirect(url_for("bills.pay_share", share_id=share_id))

        share.payment_image = payment_image.read()
        share.share_paid = True
        db.session.commit()
        bill = share.bill

        if all(s.share_paid for s in bill.shares):
            bill.shares_paid_status = "paid"
            db.session.commit()

        flash("Your share payment has been marked as paid!")
        return redirect(url_for("bills.bills_dashboard"))
    return render_template("pay_share.html", share=share)


@bills_bp.route("/reject_share/<int:share_id>")
@login_required
def reject_share(share_id):
    share = BillShare.query.get_or_404(share_id)

    if share.user_id != current_user.id:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    bill = share.bill

    bill.is_draft = True
    bill.shares_paid_status = "rejected"

    message = (
        f"{current_user.username} has rejected your bill: '{bill.title}'."
    )
    notification = Notification(user_id=bill.creator_id, message=message)
    db.session.add(notification)

    send_email(
        subject="Bill Assignment Rejected",
        recipient=bill.creator.email,
        email_body=message,
    )
    db.session.commit()
    flash(
        "You have rejected this bill. It has been returned to the creator's "
        "drafts."
    )
    return redirect(url_for("bills.bills_dashboard"))


@bills_bp.route("/paid_bill_image/<int:bill_id>")
@login_required
def paid_bill_image(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    allowed_user_ids = [share.user_id for share in bill.shares]
    allowed_user_ids += [bill.creator_id]

    if current_user.id not in allowed_user_ids:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    if not bill.payment_image:
        flash("No image found for this bill.")
        return redirect(url_for("bills.bills_dashboard"))
    return send_file(io.BytesIO(bill.payment_image), mimetype="image/jpeg")


@bills_bp.route("/paid_share_image/<int:share_id>")
@login_required
def paid_share_image(share_id):
    share = BillShare.query.get_or_404(share_id)
    bill = share.bill

    if share.user_id != current_user.id and bill.creator_id != current_user.id:
        flash("Unauthorised access.")
        return redirect(url_for("bills.bills_dashboard"))

    if not share.payment_image:
        flash("No image found for this bill share.")
        return redirect(url_for("bills.bills_dashboard"))
    return send_file(io.BytesIO(share.payment_image), mimetype="image/jpeg")
