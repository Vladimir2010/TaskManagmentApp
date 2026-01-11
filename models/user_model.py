import bcrypt
from models.database import db

class UserModel:
    def __init__(self, id=None, username="", password_hash="", role="user", email="", cloud_id=None, last_sync=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.cloud_id = cloud_id
        self.last_sync = last_sync

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def save(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, email, cloud_id, last_sync)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.username, self.password_hash, self.role, self.email, self.cloud_id, self.last_sync))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE users SET username=?, password_hash=?, role=?, email=?, cloud_id=?, last_sync=?
                WHERE id=?
            ''', (self.username, self.password_hash, self.role, self.email, self.cloud_id, self.last_sync, self.id))
            
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_username(username):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return UserModel(row['id'], row['username'], row['password_hash'], row['role'], row['email'], row['cloud_id'], row['last_sync'])
        return None
    
    @staticmethod
    def get_all():
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [UserModel(row['id'], row['username'], row['password_hash'], row['role'], row['email'], row['cloud_id'], row['last_sync']) for row in rows]
