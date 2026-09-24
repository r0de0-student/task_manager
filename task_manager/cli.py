from typing import List, Optional
from datetime import date

from .models import Task, Priority, PRIORITY_ORDER
from .storage import Storage


class TaskManager:
    def __init__(self, storage: Storage):
        # Композиция: TaskManager использует Storage, но не наследуется от него,
        # такой подход называется "внедрение зависимости" (dependency injection).
        # Плюс: легко подменить Storage на другое хранилище (например, БД).
        self.storage = storage

    def _next_id(self, tasks: List[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    # Добавили параметр due — опциональный. Если None, задача без дедлайна.
    def add(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due: Optional[date] = None,
    ) -> Task:
        tasks = self.storage.load()
        task = Task(id=self._next_id(tasks), title=title, priority=priority, due=due)
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list(self) -> List[Task]:
        return self.storage.load()

    def filter(self, done: bool) -> List[Task]:
        tasks = self.storage.load()
        return [t for t in tasks if t.done == done]

    def filter_overdue(self) -> List[Task]:
        # Задачи, у которых is_overdue() возвращает True.
        # Метод-предикат работает как условие в списковом включении.
        tasks = self.storage.load()
        return [t for t in tasks if t.is_overdue()]

    def sorted_by_priority(self, tasks: List[Task] | None = None) -> List[Task]:
        # Сортировка: сначала просроченные (по дате дедлайна), потом по приоритету.
        #
        # key — функция, возвращающая кортеж. sorted сравнивает кортежи по
        # первому элементу, потом по второму, и так далее.
        #
        # Первый элемент: 0 для просроченных, 1 для остальных.
        #   → просроченные всегда вверху.
        # Второй элемент: для просроченных — дата дедлайна (чем раньше, тем выше),
        #   для остальных — инверсия приоритета (3, 2, 1, чтобы high был первым).
        if tasks is None:
            tasks = self.storage.load()

        def sort_key(t: Task):
            overdue_priority = 0 if t.is_overdue() else 1
            # date.min — самая ранняя возможная дата. Нужна как "заглушка"
            # для задач без дедлайна, чтобы они не ломали сортировку.
            due_for_sort = t.due if t.due else date.max
            return (
                overdue_priority,
                due_for_sort,
                -PRIORITY_ORDER[t.priority],
            )

        return sorted(tasks, key=sort_key)

    def done(self, task_id: int) -> Task:
        tasks = self.storage.load()
        for t in tasks:
            if t.id == task_id:
                t.done = True
                self.storage.save(tasks)
                return t
        raise ValueError(f"Задача с id={task_id} не найдена")

    def delete(self, task_id: int) -> None:
        tasks = self.storage.load()
        new_tasks = [t for t in tasks if t.id != task_id]
        if len(new_tasks) == len(tasks):
            raise ValueError(f"Задача с id={task_id} не найдена")
        self.storage.save(new_tasks)