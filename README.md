# Pilot Fastenal Scraper

## Overview
Pilot Fastenal Scraper is a Python project designed to scrape data from the Fastenal website. This tool allows users to extract product information, pricing, and availability from Fastenal's online catalog.

## Installation
To get started with the Pilot Fastenal Scraper, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pilot_fastenal_scrapper.git
   ```
2. Navigate into the project directory:
   ```
   cd pilot_fastenal_scrapper
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the scraper, execute the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.



NOTAS


SOLID Principles: The WebDriverAdapter adheres to the Single Responsibility Principle by abstracting Selenium's WebDriver. The WebScrapingService handles the scraping logic, adhering to the Open/Closed Principle.
Environment Variables: The .env file is used to manage the URL.
Adapter Pattern: The WebDriverAdapter acts as an adapter between the Selenium WebDriver and the scraping service.


TODO: Agregar logs (no estandarizados)
TODO: Alertas en caso de falla en scrapping
