import requests, httpx, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectionServer:
    def __init__(self):
        pass

    def fetchw(lib, url):
        if lib == "requests":
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
        else:
            logging.error("Uso Incorreto No Metodo Fetchw")
            return None