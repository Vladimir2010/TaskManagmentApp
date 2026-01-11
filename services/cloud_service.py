import requests
from config import Config

class CloudService:
    @staticmethod
    def register(username, password):
        try:
            response = requests.post(f"{Config.CLOUD_API_URL}/register", json={
                "username": username,
                "password": password
            })
            if response.status_code == 201:
                return True, response.json()
            return False, response.json().get("error", "Unknown error")
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login(username, password):
        try:
            response = requests.post(f"{Config.CLOUD_API_URL}/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                return True, response.json()
            return False, response.json().get("error", "Login failed")
        except Exception as e:
            return False, str(e)
            
    @staticmethod
    def sync_tasks(tasks, token):
        # Implementation of sync logic
        try:
            response = requests.post(f"{Config.CLOUD_API_URL}/sync", json={"tasks": tasks}, headers={"Authorization": token})
            return response.status_code == 200
        except:
            return False
