# WatchFacts Hermes AI Platform

This is the phase 1 prototype of the Hermes AI Platform for WatchFacts. It simulates the core functionality required to resolve exceptions from WhatsApp dealer listings and provides a unified dashboard and seller app.

## Project Structure

*   `database.py`: SQLAlchemy models and SQLite database initialization. Includes seed data for the master catalog.
*   `synthetic_data.py`: Script to generate 1,000 synthetic watch listings, simulating both clean and messy (exception) data.
*   `resolver.py`: The Hermes AI Exception Resolver engine. Simulates AI logic to fix common errors (nicknames, catalog mismatches).
*   `dashboard.py`: Streamlit application serving as the Admin Dashboard for viewing metrics and resolving exceptions.
*   `seller_app.py`: Streamlit application simulating the mobile-first Seller App experience.

## Quickstart

1.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install sqlalchemy faker streamlit pandas plotly
    ```
3.  Initialize the database and generate synthetic data:
    ```bash
    python database.py
    python synthetic_data.py
    ```
4.  Run the batch resolver to auto-resolve some exceptions:
    ```bash
    python resolver.py
    ```
5.  Run the Admin Dashboard:
    ```bash
    streamlit run dashboard.py
    ```
6.  Run the Seller App (in a separate terminal):
    ```bash
    streamlit run seller_app.py
    ```
