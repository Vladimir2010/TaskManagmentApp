from models.task_model import TaskModel

class TaskController:
    def __init__(self):
        pass

    def get_user_tasks(self, user_id):
        return TaskModel.get_by_user(user_id)

    def create_task(self, user_id, title, description, due_date, priority, category):
        task = TaskModel(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category
        )
        task.save()
        return task

    def update_task(self, task_id, **kwargs):
        task = TaskModel.get_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            task.save()
            return True
        return False

    def delete_task(self, task_id):
        task = TaskModel.get_by_id(task_id)
        if task:
            task.delete()
            return True
        return False
    
    def get_statistics(self, user_id):
        tasks = self.get_user_tasks(user_id)
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == "Completed")
        pending = total - completed
        return {"total": total, "completed": completed, "pending": pending}
