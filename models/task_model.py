from models.database import db

class TaskModel:
    def __init__(self, id=None, user_id=None, title="", description="", due_date="", priority="Medium", status="Pending", category="General", is_synced=0, cloud_id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.category = category
        self.is_synced = is_synced
        self.cloud_id = cloud_id
        self.created_at = created_at

    def save(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO tasks (user_id, title, description, due_date, priority, status, category, is_synced, cloud_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.user_id, self.title, self.description, self.due_date, self.priority, self.status, self.category, self.is_synced, self.cloud_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE tasks SET user_id=?, title=?, description=?, due_date=?, priority=?, status=?, category=?, is_synced=?, cloud_id=?
                WHERE id=?
            ''', (self.user_id, self.title, self.description, self.due_date, self.priority, self.status, self.category, self.is_synced, self.cloud_id, self.id))
            
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [TaskModel(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(task_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return TaskModel(**dict(row))
        return None
