Bill Splitter Deluxe

A secure, collaborative expense-sharing and bill-splitting web application built
with Python and the Flask framework. This application enables groups,
housemates, or families to split shared costs, upload payment verification,
track debts across distinct statuses (Overdue, Late Payment, Due, Paid on Time),
and manage disputes via a collaborative rejection workflow.

Key Features

👥 Collaborative Expense Management

  - Split Calculations: Creators can select multiple users to split a bill. The
    system automatically distributes the cost evenly between the assigned payees
    and the creator.
  - State-Driven Rejection Workflow: To prevent spam or incorrect expense logs,
    payees have the authority to reject bill shares. Rejecting a bill
    immediately updates its state, sends email and in-app notifications to the
    creator, and reverts the bill back to the creator's drafts with a red
    (Rejected) flag for adjustments and resubmission.
  - Receipt Verification: For accountability, uploading a payment proof image is
    compulsory. Image assets are securely served via authorization-locked
    backend routes rather than public directory exposure.

📊 Dynamic User Dashboard

  - Status-based Tracking: Clear tabular views displaying outstanding, overdue,
    or paid balances based on real-time comparison with due dates.
  - Interactive Controls: Built-in AJAX-driven category filters (Utilities,
    Rent, Groceries, Entertainment, Other) allow users to filter dashboard
    tables instantly without page reloads.
  - In-app Notifications: Real-time updates via a dashboard notification bell
    (unread alerts transition to "read" state instantly via an asynchronous POST
    request).

🛡️ Security & Authentication

  - Role-based Access Control: Clear division between normal users and
    administrators. Admin panels and metrics are strictly isolated behind custom
    decorators.
  - Secure Authentication: User accounts feature password hashing using
    Werkzeug. Session state is managed securely with Flask-Login.
  - Token-based Password Recovery: Secure password recovery system generating
    safe, time-expiring url tokens for email-based resets.
  - Audit Logging: Tracks successful and unsuccessful login attempts, logging
    attempted emails, user IDs, and timestamps. Unregistered email attempts are
    flagged separately in an admin-facing Security Risks Log.

⚙️ Administrative Dashboard

  - User Oversight: Administrators can audit all registered users, inspect their
    login history, and review their created bills.
  - Actionable Tools: Admins have the authority to permanently delete bills or
    archive them (forcing them back to draft status).

Architecture & Design Patterns

  - Application Factory Pattern: Built using Flask’s standard create_app()
    factory method to safely register blueprints and initialize extension
    instances (SQLAlchemy, LoginManager, Mail) globally while avoiding circular
    dependencies.
  - Blueprint Modularization: Separates distinct features (auth, bills, admin)
    into independent modules, simplifying extension and code review.
  - ORM Layer: Uses SQLAlchemy with custom property helper methods on models
    (such as tracking unread notifications or calculating dynamic individual
    bill share statuses).
  - Environment Isolation: All sensitive configuration data, mail servers, and
    secret keys are loaded from an ignored .env file via python-dotenv.

Installation & Setup

Prerequisites

  - Python 3.10 or higher
  - pip (Python package manager)

1. Setup Environment & Initialize Database

Clone this repository, navigate to the root directory, and run the following
commands to set up your virtual environment, install dependencies, and run the
schema setup:

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows: venv\Scripts\activate
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run CLI command to initialize database schema and seed default admin user
flask init-db

Note: The default administrator credentials are initialized as admin@example.com
/ Password123.

2. Configure Environment Variables

Create a .env file in the root folder (or copy .env.example) to hold local
configuration settings:

FLASK_APP=app
FLASK_DEBUG=true
SECRET_KEY=this_should_be_a_secret_key
DATABASE_URL=sqlite:///billsplitter.db
MAIL_SUPPRESS_SEND=false
MAIL_SERVER=127.0.0.1
MAIL_PORT=8025

3. Run a Local Mail Server for Testing

To test automated notification emails and password resets locally [1]:

1.  Open a separate terminal window.
2.  Run the mock SMTP server on port 8025 [1]:
    python -m aiosmtpd -n -l 127.0.0.1:8025

4. Run the Application

With your primary terminal's virtual environment activated, boot the Flask
development server:

flask run

Open your browser and navigate to the local server output link (typically
http://127.0.0.1:5000).
