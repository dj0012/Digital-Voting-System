import os
import json
import hashlib
import mysql.connector as connector

DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root123",
    "database": "voting_system"
}

def load_db_config():
    """Loads database config from config.json and optional environment variables."""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    config = DEFAULT_CONFIG.copy()

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                for key, val in file_config.items():
                    if key in DEFAULT_CONFIG:
                        config[key] = val
        except Exception:
            pass

    env_map = {
        "host": "DB_HOST",
        "port": "DB_PORT",
        "user": "DB_USER",
        "password": "DB_PASSWORD",
        "database": "DB_NAME"
    }

    for key, env_name in env_map.items():
        value = os.getenv(env_name)
        if value is not None and value != "":
            config[key] = int(value) if key == "port" else value

    return config

def get_db_connection():
    """Returns a secure database connection using the external config."""
    cfg = load_db_config()
    return connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"]
    )

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2 HMAC SHA-256 with a unique random salt."""
    if not password:
        return ""
    # Generate random salt (16 bytes in hex)
    salt = os.urandom(16).hex()
    # Hash password
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Number of iterations
    )
    return f"{salt}:{hash_bytes.hex()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a password against a stored PBKDF2 HMAC SHA-256 hash."""
    if not stored_password or not provided_password:
        return False
    
    if ':' not in stored_password:
        return False
        
    try:
        salt, stored_hash = stored_password.split(':', 1)
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hash_bytes.hex() == stored_hash
    except Exception:
        return False
