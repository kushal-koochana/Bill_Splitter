import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-insecure-key-for-dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///billsplitter.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER", "noreply@billsplitter.com"
    )
    MAIL_SUPPRESS_SEND = os.environ.get(
        "MAIL_SUPPRESS_SEND", "True"
    ).lower() in ("true", "1")

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "127.0.0.1")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 8025))
