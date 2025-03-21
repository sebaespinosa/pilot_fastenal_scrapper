# Pilot Fastenal Scraper

## Overview
Pilot Fastenal Scraper is a Python project designed to scrape data from the Fastenal website. This tool allows users to extract product information, pricing, and availability from Fastenal's online catalog.

When executed, information is store in a Google Sheet to perfomr further and historical analysis.

A Price Analyze script it's available. It check the latest product price, calculate the average price of the product during the past X days where X is defined on the environment variables. If the current price is lower o higher by percentaje threshold defined on environmente variables, and alarm is triggered.

## Installation
To get started with the Pilot Fastenal Scraper, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/sebaespinosa/pilot_fastenal_scrapper.git
   ```
2. Navigate into the project directory:
   ```
   cd pilot_fastenal_scrapper
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a copy of the .env.example file named .env and fill in the variable information.
5. Either create a new Google Sheet or connect to existing one by following the instructions on [GoogleSheetSetUp.md](GoogleSheetSetUp.md)
6. Fill the information on the .env file, including the credentials file generated. 

## Usage
To run the scraper, execute the following command:
```
python src/main.py
```
To run the price analysis, execute the following command:
```
python src/price_analyze.py
```

## Notes and considerations
Since this is only a pilot, please be aware of the following considerations and possible improvements
- No Unit Testing or other testing was included
- No logging was implemented, just simple console prints
- Improvementes needed to handle cases with multiple prices like [https://www.fastenal.com/product/details/0557302], I also assume the information for "Product Description Text" and "Product Manufacterer", could be another fields.
- To avoid blocking and get the information, a hardcoded waiting between each page navigation is implemented. This can be improved/optimized.
- Alerts on failures and prices changes, for now are just console prints. More advance notification systems are possible.
- Same applies for how the alarm are generated. I used a comparission with the average price just as example.
```
ALARM: SKU 0546940 has a current price of 105.00, which deviates from the 7-day average price of 100.00.
ALARM: No data available older than 7 days. Stopping the process.
```
- Since I have only one day of data, it was not possible to test further the price analysis. Same as with Testing, no data mocking was implemented to test since it's a pilot.
- For sure there are more border cases to cover and things to review like price format. For that it's necesarry to collect more date during a longer period of time.