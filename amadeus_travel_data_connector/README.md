# Amadeus Travel Data Connector

A minimal Python tool to fetch flight and hotel data from the Amadeus API, merge them into package combinations, and generate a summary report.

## Prerequisites

- Python 3.x
- [Amadeus for Developers](https://developers.amadeus.com/) API credentials.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure environment variables:**
    Create a `.env` file in the root directory (if it doesn't already exist) and add your Amadeus API credentials:
    ```env
    AMADEUS_API_KEY=your_api_key_here
    AMADEUS_API_SECRET=your_api_secret_here
    ```

## Usage

Run the main script to fetch data and generate the report:
```bash
python main.py
```

The script will fetch flight and hotel information for a predefined route and date, merge the results, and print a summary report to the terminal.
