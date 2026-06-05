import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
    VALID_USERNAME = os.getenv("VALID_USERNAME", "admin")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD", "admin")