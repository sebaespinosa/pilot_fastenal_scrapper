import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from collections import defaultdict

def price_analyze():
    """
    Connects to the Google Sheet, retrieves product data, and analyzes price changes.
    Prints an alarm if the current price deviates by more than the threshold from the average price
    over the last X days, where X is defined in the environment variable TIMEFRAMECHECK.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get credentials file, sheet name, alarm threshold, and timeframe from environment variables
    credentials_file = os.getenv("CREDENTIALS_FILE")
    sheet_name = os.getenv("SHEET_NAME")
    alarm_threshold = os.getenv("ALARM_THRESHOLD")
    timeframe_check = os.getenv("TIMEFRAMECHECK")

    if not credentials_file or not sheet_name or not alarm_threshold or not timeframe_check:
        raise ValueError("CREDENTIALS_FILE, SHEET_NAME, ALARM_THRESHOLD, and TIMEFRAMECHECK must be set in the .env file.")

    try:
        # Convert alarm_threshold to a float and timeframe_check to an integer
        alarm_threshold = float(alarm_threshold) / 100  # Convert percentage to decimal
        timeframe_check = int(timeframe_check)  # Convert timeframe to an integer
    except ValueError:
        raise ValueError("ALARM_THRESHOLD must be a valid number and TIMEFRAMECHECK must be a valid integer.")

    # Authenticate and connect to the Google Sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1

    # Get all rows from the sheet
    rows = sheet.get_all_values()

    # Extract the header and data rows
    header = rows[0]
    data = rows[1:]

    # Column indices based on the header (1-based indexing in Google Sheets)
    sku_col = header.index("SKU") + 1
    price_col = header.index("Price") + 1
    date_col = header.index("RecordDate") + 1

    # Parse the data into a dictionary grouped by SKU
    product_data = defaultdict(list)
    for row in data:
        try:
            sku = row[sku_col - 1]
            price = float(row[price_col - 1])
            date = datetime.strptime(row[date_col - 1], "%m/%d/%Y")
            product_data[sku].append((date, price))
        except (ValueError, IndexError):
            # Skip rows with invalid data
            continue

    # Get the last available date in the sheet
    last_date = max(date for sku_data in product_data.values() for date, _ in sku_data)

    # Check if there is data older than the timeframe_check
    oldest_date = last_date - timedelta(days=timeframe_check)
    has_old_data = any(
        any(date <= oldest_date for date, _ in records)
        for records in product_data.values()
    )

    if not has_old_data:
        print(f"ALARM: No data available older than {timeframe_check} days. Stopping the process.")
        return

    # Analyze prices for each product
    for sku, records in product_data.items():
        # Filter records for the last X days (defined by TIMEFRAMECHECK)
        last_x_days = [
            price for date, price in records
            if last_date - timedelta(days=timeframe_check) <= date <= last_date
        ]

        if len(last_x_days) > 0:
            # Calculate the average price for the last X days
            average_price = sum(last_x_days) / len(last_x_days)

            # Get the current price (price on the last available date)
            current_price = next(
                price for date, price in records if date == last_date
            )

            # Check if the price deviates by more than the threshold
            if abs(current_price - average_price) / average_price > alarm_threshold:
                print(
                    f"ALARM: SKU {sku} has a current price of {current_price:.2f}, "
                    f"which deviates from the {timeframe_check}-day average price of {average_price:.2f} "
                    f"by more than {alarm_threshold * 100:.2f}%."
                )

price_analyze()