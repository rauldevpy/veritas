import re, string, json
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SelectorsManager:
    def __init__(self):
        pass

    def searchw(self, type, arg, html):
        try:
            if type == "regex":
                logging.info("Campos Encontrados Com Regex")
                resultados = {}
                campos = {k: v["stringValue"] for k, v in arg.items()}
                for campo, pattern in campos.items():
                    encontrados = re.findall(pattern, html, re.DOTALL)
                    resultados[campo] = encontrados
                return resultados if any(resultados.values()) else None

            elif type == "bs4":
                soup = BeautifulSoup(html, "html.parser")
                resultados = {}
                campos = {k: v["stringValue"] for k, v in arg.items()}
                for campo, seletor in campos.items():
                    encontrados = soup.select(seletor)
                    resultados[campo] = [e.get_text(strip=True) for e in encontrados]
                return resultados if any(resultados.values()) else None

        except Exception as e:
            logging.error(f"Erro: {e}")
            return None