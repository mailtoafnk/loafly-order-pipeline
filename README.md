# Loafly Order Pipeline

A small, production-ready Python package that reads the day's bakery orders,
cleans the prices, applies a discount, and saves each order to the orders API
with retry. Python standard library only.

## Project layout

```
loafly/
    __init__.py     makes loafly a package
    config.py       all settings in one SETTINGS dict + reads the API key
    models.py       the Order class
    extract.py      reads raw_orders.csv
    transform.py    cleans prices, skips bad items, builds Order objects
    load.py         applies the discount, saves each order with retry
run_pipeline.py     runs extract -> transform -> load
gateway.py          provided orders-API client (not edited)
raw_orders.csv      input data
env.example         template for the .env secrets file
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Mac / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install requirements (standard library only, so this installs nothing):

   ```bash
   pip install -r requirements.txt
   ```

3. Create your secrets file from the template and set the real key:

   ```bash
   copy env.example .env      # Windows
   cp env.example .env        # Mac / Linux
   ```

   `.env` is git-ignored and must never be committed.

## Run

```bash
python run_pipeline.py
```

Logs are printed to the terminal and written to `loafly.log`.

## Design decisions

- **Config-driven:** every setting (currency, discount, input file, retries,
  wait time, log file) lives in `SETTINGS` in `config.py`. Change it there and
  behaviour changes without touching other files.
- **Exception handling:** a missing or unreadable price raises `ValueError`
  (e.g. `float("")`). It is caught, logged as a WARNING, and only that item is
  skipped, so the run always completes.
- **Retry:** the flaky `save_to_orders_api` call is tried up to `max_retries`
  times, waiting `retry_wait_seconds` between attempts. Each failure is a
  WARNING; giving up is an ERROR, and the pipeline moves on to the next order.
- **Secrets:** the API key is read with `os.getenv("LOAFLY_API_KEY")` after a
  small standard-library loader copies values from `.env` into the
  environment. Only the last 4 characters are ever logged.
