"""config.py - every setting the pipeline needs, in one place.

Change a value here and the pipeline's behaviour changes -
no other file needs editing. Secrets are NOT stored here: they are
read from the environment (or a git-ignored .env file).
"""
import os

SETTINGS = {
    "input_file": "raw_orders.csv",   # where today's orders come from
    "currency": "INR",                # shown next to every total
    "discount_percent": 10,           # taken off every order total
    "max_retries": 3,                 # attempts to save one order
    "retry_wait_seconds": 1,          # pause between attempts
    "log_file": "loafly.log",         # where the run log is written
    "log_level": "INFO",              # DEBUG, INFO, WARNING, ERROR
    "env_file": ".env",               # local secrets file (never committed)
}


def load_env_file(path):
    """Copy KEY=value lines from a .env file into os.environ.

    Standard library only (no python-dotenv). Blank lines and # comments
    are ignored, and a variable already set in the real environment wins.
    """
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file(SETTINGS["env_file"])

# The secret: read from the environment, never typed into the code.
API_KEY = os.getenv("LOAFLY_API_KEY", "demo-key")