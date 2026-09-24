import json
from pathlib import Path # pathlib.Path — современная замена os.path для работы с путями
from typing import List # typing.List — устаревший способ аннотировать список
from .models import Task # Относительный импорт (точка перед models) — импорт из того же пакета

class Storage:
    def __init__(self, path: str | Path = "tasks.json"):
        self.path = Path(path)

    def load(self) -> List[Task]:
        # Если файла ещё нет (первый запуск) — возвращаем пустой список.
        # Это нормальная ситуация, а не ошибка.
        if not self.path.exists():
            return []

        try:
            # read_text читает весь файл в одну строку.
            raw = self.path.read_text(encoding="utf-8")
            data = json.loads(raw)  # json.loads превращает строку JSON в Python-объект (список словарей).
        except json.JSONDecodeError:
            # Файл есть, но внутри невалидный JSON (например, пользователь его сломал) не падаем — просто считаем, что задач нет.
            return []
        return [Task.from_dict(item) for item in data] # Списковое включение (list comprehension): из каждого словаря делаем Task

    def save(self, tasks: List[Task]) -> None:
        # Превращаем список объектов Task в список словарей.
        data = [t.to_dict() for t in tasks]
        # json.dumps превращает Python-объект в строку JSON
        text = json.dumps(data, ensure_ascii=False, indent=2)
        self.path.write_text(text, encoding="utf-8")