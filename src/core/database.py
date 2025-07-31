import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataManager:
    def __init__(self):
        pass
    
    def load(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        file = os.path.join(base, "server.json")
        try:
            with open(file, "r") as f:
                data = json.load(f)
                email = data.get("user")
                password = data.get("pass")
                api_key = data.get("apikey")
                projeto = data.get("projeto")
        
                if not all([email, password, api_key]):
                    raise ValueError("Algumas configurações estão faltando no arquivo de configuração.")
        
                logging.info("Configurações carregadas com sucesso.")
                return email, password, api_key, projeto
        except FileNotFoundError:
            logging.error(f"Erro: server.json inexistente. {base}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Erro: Arquivo {base} corrompido.")
            raise
        except ValueError as e:
            logging.error(f"Erro: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro: {e}")
            raise

    def login(self, email, password, api_key):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            res = requests.post(url, json=payload)
            res.raise_for_status()
            data = res.json()
            logging.info("Login realizado com sucesso.")
            return data["idToken"]
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro: {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Erro de conexão: {e}")
            raise
        except (KeyError, ValueError) as e:
            logging.error(f"Erro: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro: {e}")
            raise
    
    def get_feed(self, filter, arg):
        e, p, a, pp = self.load()
        url = f"https://firestore.googleapis.com/v1/projects/{pp}/databases/(default)/documents/feeds/"
        token = self.login(e, p, a)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            docs = res.json().get("documents", [])
            for doc in docs:
                fields = doc.get("fields", {})

                if filter == "By_NAME":
                    nome = fields.get("nome", {}).get("stringValue", "")
                    if nome == arg:
                        logging.info(f"Feed Encontrado por nome: {nome}")
                        return fields
                    
                elif filter == "By_TIPO":
                    tipo = fields.get("tipo", {}).get("stringValue", "")
                    if tipo == arg:
                        logging.info(f"Feed Encontrado por tipo: {tipo}")
                        return fields
                
                elif filter == "URL":
                    fonte = fields.get("fonte", {}).get("mapValue", {}).get("fields", {})
                    url = fonte.get("url", {}).get("stringValue", "")
                    if url == arg:
                        logging.info(f"Feed Encontrado por url: {url}")
                        return fields

            logging.warning(f"Nenhum resultado encontrado para {filter} = {arg}")
            return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro: {e}")
            return None

    def get_selectors(self, filter, arg):
        e, p, a, pp = self.load()
        url = f"https://firestore.googleapis.com/v1/projects/{pp}/databases/(default)/documents/feeds/"
        token = self.login(e, p, a)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            docs = res.json().get("documents", [])
            for doc in docs:
                fields = doc.get("fields", {})

                if filter == "By_NAME":
                    nome = fields.get("nome", {}).get("stringValue", "")
                    if nome == arg:
                        logging.info(f"Feed Encontrado por nome: {nome}")
                        return fields["alvos"]["mapValue"]["fields"]
                    
                elif filter == "By_TIPO":
                    tipo = fields.get("tipo", {}).get("stringValue", "")
                    if tipo == arg:
                        logging.info(f"Feed Encontrado por tipo: {tipo}")
                        return fields["alvos"]["mapValue"]["fields"]
                
                elif filter == "URL":
                    fonte = fields.get("fonte", {}).get("mapValue", {}).get("fields", {})
                    url = fonte.get("url", {}).get("stringValue", "")
                    if url == arg:
                        logging.info(f"Feed Encontrado por url: {url}")
                        return fields["alvos"]["mapValue"]["fields"]

            logging.warning(f"Nenhum resultado encontrado para {filter} = {arg}")
            return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro: {e}")
            return None
    
    def get_feeds(self):
        all = []
        e, p, a, pp = self.load()
        url = f"https://firestore.googleapis.com/v1/projects/{pp}/databases/(default)/documents/feeds/"
        token = self.login(e, p, a)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            docs = res.json().get("documents", [])
            for doc in docs:
                fields = doc.get("fields", {})
                nome = fields.get("nome", {}).get("stringValue", "")
                url = fields.get("fonte", {}).get("mapValue", {}).get("fields", {}).get("url", {}).get("stringValue", "")
                all.append({"nome": nome, "url": url})
            
            if all:
                logging.info("Feeds Enviados Para a Aplicação.")
                return all
            else:
                logging.error("Nenhum Feed Na Database")
                return None
        except Exception as e:
            logging.error(f"Erro: {e}")
            return None