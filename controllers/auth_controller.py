from models.user_model import UserModel
from services.cloud_service import CloudService

class AuthController:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        # Local Login
        user = UserModel.get_by_username(username)
        if user and UserModel.verify_password(password, user.password_hash):
            self.current_user = user
            return True, "Login successful"
        
        # If not found locally, try cloud (Optional hybrid approach, keeping strictly local first for this requirements)
        # But per requirements, we sync. For now, strict local + sync later.
        
        return False, "Invalid username or password"

    def register(self, username, password, email):
        if UserModel.get_by_username(username):
            return False, "Username already exists"
        
        # Hash password
        hashed = UserModel.hash_password(password)
        
        # Create User
        new_user = UserModel(username=username, password_hash=hashed, email=email)
        new_user.save()
        
        # Try register on cloud
        success, _ = CloudService.register(username, password)
        if success:
            # Update cloud_id if we were fully implementing bi-directional sync registration linkage here
            pass

        return True, "Registration successful"

    def logout(self):
        self.current_user = None
