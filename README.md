# Bill Splitter — Collaborative Expense Management System

A secure, collaborative expense-sharing web application built with **Python**, **Flask**, and **SQLAlchemy**. Bill Splitter enables groups, housemates, and families to manage shared expenses efficiently through automatic bill splitting, payment verification, dispute management, notifications, and an administrative dashboard.

The project demonstrates full-stack web development principles including authentication, authorisation, database design, asynchronous requests (AJAX), secure file handling, and modular application architecture using the Flask Application Factory pattern.

---

## Features

### 👥 Collaborative Expense Management

- Create bills and split costs evenly between multiple users.
- Automatic calculation of individual payment shares.
- Upload payment verification images for accountability.
- Secure receipt access through authenticated backend routes.
- Collaborative rejection workflow allowing users to dispute incorrect bill shares.
- Rejected bills are automatically returned to the creator as drafts for editing and resubmission.

### 📊 Interactive Dashboard

- View bills grouped by payment status:
  - Due
  - Paid on Time
  - Late Payment
  - Overdue
- AJAX-powered category filtering without requiring page reloads.
- Real-time notification system with unread/read status updates.
- Clear overview of outstanding balances and payment history.

### 🔐 Authentication & Security

- Secure user authentication using Flask-Login.
- Password hashing via Werkzeug.
- Time-limited password reset tokens.
- Role-based access control separating administrator and standard user functionality.
- Login audit logging for both successful and failed authentication attempts.
- Administrative Security Risks Log for monitoring suspicious login activity.

### ⚙️ Administrative Features

Administrators can:

- View all registered users
- Inspect login history
- Review user-created bills
- Delete bills
- Archive bills back to draft status
- Monitor authentication activity

---

## Technologies

### Backend

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Mail

### Frontend

- HTML5
- CSS3
- JavaScript
- AJAX
- Jinja2 Templates

### Database

- SQLite

### Development Tools

- python-dotenv
- aiosmtpd (local email testing)

---

## Project Architecture

The application follows Flask's recommended **Application Factory** architecture.

```

Client (Browser)
│
├── HTML
├── CSS
└── JavaScript (AJAX)
        │
        ▼
Flask Application
        │
        ├── Authentication Blueprint
        ├── Bills Blueprint
        ├── Admin Blueprint
        │
        ▼
SQLAlchemy ORM
        │
        ▼
SQLite Database

```

This modular structure improves maintainability, simplifies testing, and avoids circular dependencies by registering extensions through a central `create_app()` factory.

---
## Project Structure

```
Bill_Splitter/
│
├── app/
│   ├── routes/              # Flask blueprints
│   ├── static/              # CSS, JavaScript and uploaded receipts
│   ├── templates/           # Jinja2 templates
│   ├── config.py            # Application configuration
│   ├── extensions.py        # Flask extensions
│   ├── models.py            # SQLAlchemy models
│   ├── utils.py             # Helper functions
│   └── __init__.py          # Application factory
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Prerequisites

Before running the application, ensure you have:

- Python 3.10 or later
- pip

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Bill_Splitter
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Typical configuration includes:

```env
SECRET_KEY=your_secret_key

MAIL_SERVER=127.0.0.1
MAIL_PORT=8025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@example.com
```

The `.env` file is ignored by Git to prevent sensitive configuration data from being committed.

### 5. Initialise the Database

Run the custom Flask CLI command:

```bash
flask init-db
```

This creates the database schema and seeds the default administrator account.

Default administrator credentials:

```
Email: admin@example.com
Password: Password123
```

> It is recommended to change these credentials before deploying the application.

---

## Running a Local Mail Server

Password reset emails and notification emails can be tested locally using **aiosmtpd**.

Open a second terminal and run:

```bash
python -m aiosmtpd -n -l 127.0.0.1:8025
```

The application will send emails to this local SMTP server during development.

---

## Running the Application

With the virtual environment activated, start the Flask development server:

```bash
flask run
```

The application will be available at:

```
http://127.0.0.1:5000
```

Open this address in your web browser to begin using the application.

---

## Security Features

Bill Splitter incorporates several security measures commonly used in modern web applications.

### Authentication

- Password hashing using Werkzeug
- Secure session management with Flask-Login
- Time-limited password reset tokens
- Login required decorators protecting authenticated routes

### Authorisation

- Administrator-only routes protected using custom decorators
- Restricted access to uploaded payment receipts
- Role-based access control throughout the application

### Audit Logging

The application records:

- Successful login attempts
- Failed login attempts
- Login timestamps
- User identifiers
- Unregistered email login attempts

This information is available through the administrator Security Risks Log for auditing and monitoring.

---

## Design Principles

The application was designed with maintainability, security, and modularity in mind.

### Flask Application Factory

The project uses Flask's `create_app()` factory pattern to:

- Initialise Flask extensions in a single location
- Register blueprints cleanly
- Reduce circular dependencies
- Improve maintainability and scalability

### Blueprints

Application functionality is separated into dedicated blueprints:

- Authentication
- Bills
- Administration

This modular design keeps related functionality together and simplifies future development.

### SQLAlchemy ORM

SQLAlchemy is used to model the application's database entities and relationships.

Model helper methods are used where appropriate to simplify business logic, such as calculating payment statuses and retrieving unread notifications.

### Environment Configuration

Sensitive configuration values, including secret keys and mail settings, are loaded from a `.env` file using `python-dotenv`.

This prevents confidential information from being committed to version control.

---

## Future Improvements

Potential future enhancements include:

- Responsive mobile-first interface
- Docker deployment
- PostgreSQL support
- Continuous Integration using GitHub Actions
- Enhanced reporting and analytics
- Recurring bills
- Multi-currency support
- Exporting bills and payment history as PDF

---

## Screenshots

Screenshots of the application can be added here.

### Login Page

*Add screenshot*

### Dashboard

*Add screenshot*

### Bill Creation

*Add screenshot*

### Notifications

*Add screenshot*

### Administrator Dashboard

*Add screenshot*

---

## Learning Outcomes

This project demonstrates practical experience with:

- Full-stack web application development
- Python programming
- Flask application architecture
- SQL database design
- SQLAlchemy ORM
- User authentication and authorisation
- Secure password management
- File upload handling
- REST-style route design
- AJAX-based asynchronous interactions
- Server-side rendering using Jinja2
- Form validation with Flask-WTF
- Email integration using Flask-Mail
- Environment variable management
- Modular software architecture

---

## Acknowledgements

This project was developed as part of university coursework to demonstrate secure web application development, collaborative software engineering principles, and modern Flask development practices.

---

## Licence

This repository is provided for educational and portfolio purposes.

Please do not copy or submit this work as your own for academic assessment.
