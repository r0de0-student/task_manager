from typing import List
from .models import Task
from .storage import Storage

class TaskManager:
    def __init__(self, storage: Storage):
        # Композиция: TaskManager использует Storage, но не наследуется от него, такой подход называется "внедрение зависимости" (dependency injection)
        # Плюс: легко подменить Storage на другое хранилище (например, БД)
        self.storage = storage

    def _next_id(self, tasks: List[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    def add(self, title: str) -> Task:
        tasks = self.storage.load()
        task = Task(id=self._next_id(tasks), title=title)
        tasks.append(task)  # append добавляет элемент в конец списка
        self.storage.save(tasks)
        return task  # Возвращаем созданную задачу

    def list(self) -> List[Task]:
        # Просто делегируем загрузку хранилищу.
        return self.storage.load()

    def filter(self, done: bool) -> List[Task]:
        # Вернуть только выполненные (done=True) или только невыполненные (done=False).
        tasks = self.storage.load()
        return [t for t in tasks if t.done == done]

    def done(self, task_id: int) -> Task:
        tasks = self.storage.load()
        for t in tasks:
            if t.id == task_id:
                t.done = True
                self.storage.save(tasks)
                return t
        # Если цикл закончился, а мы не вышли через return — задачи нет
        raise ValueError(f"Задача с id={task_id} не найдена")

    def delete(self, task_id: int) -> None:
        tasks = self.storage.load()
        # Списковое включение: оставляем все задачи, кроме той, что удаляем
        new_tasks = [t for t in tasks if t.id != task_id]
        # Если длина не изменилась — значит, задачи с таким id не было
        if len(new_tasks) == len(tasks):
            raise ValueError(f"Задача с id={task_id} не найдена")
        self.storage.save(new_tasks)
