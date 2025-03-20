from selenium import webdriver

class WebDriverAdapter:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def get_page_source(self, url: str) -> str:
        self.driver.get(url)
        return self.driver.page_source