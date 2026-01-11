import threading
import time
from services.cloud_service import CloudService
from models.task_model import TaskModel
from config import Config

class SyncController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.running = False
        self.thread = None

    def start_background_sync(self):
        self.running = True
        self.thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.thread.start()

    def stop_sync(self):
        self.running = False

    def _sync_loop(self):
        while self.running:
            self.perform_sync()
            time.sleep(Config.SYNC_INTERVAL_SECONDS)

    def perform_sync(self):
        # Get unsynced tasks
        # In a real app, this would be complex differential sync
        # Here we just push all tasks for demo
        tasks = TaskModel.get_by_user(self.user_id)
        task_data = [task.__dict__ for task in tasks]
        
        # Token handling would be needed here, passed from AuthController
        success = CloudService.sync_tasks(task_data, "token-placeholder")
        if success:
            print("Sync successful")
        else:
            print("Sync failed")
