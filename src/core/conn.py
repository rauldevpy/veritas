import httpx
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectionServer:
    def __init__(self):
        pass

    def fetchw(self, lib, url):
        if lib == "requests":
            import requests
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                return r.text
            except Exception as e:
                logging.error(e)
                return None

        elif lib == "httpx":
            try:
                r = httpx.get(url, timeout=10)
                r.raise_for_status()
                return r.text
            except Exception as e:
                logging.error(e)
                return None

        elif lib == "playwright":
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, timeout=15000)
                    html = page.content()
                    browser.close()
                    return html
            except Exception as e:
                logging.error(e)
                return None

        else:
            logging.error("Uso Incorreto No Metodo Fetchw")
            return None