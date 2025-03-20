from selenium import webdriver

class WebDriverAdapter:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def get_page_source(self, url: str) -> str:
        self.driver.get(url)
        return self.driver.page_source

    def get_page_source_async(self, url: str) -> str:
        """
        Executes an asynchronous script to get the HTML content of the page.
        Waits for at least 10 seconds before returning the result.
        """
        self.driver.get(url)
        # Execute the asynchronous script with a 10-second delay
        html_content = self.driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            setTimeout(function() {
                callback(document.getElementsByTagName('html')[0].innerHTML);
            }, 10000);  // Wait for 10 seconds (3,000 milliseconds)
        """)
        # TODO: Wait for page to finish instead of hard waiting 10 seconds
        return html_content