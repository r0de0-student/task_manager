# Path нужен для аннотации типа аргумента tmp_path
from pathlib import Path
# Импортируем наши классы из пакета task_manager
from task_manager.models import Task
from task_manager.storage import Storage
# ВАЖНО: имя функции должно начинаться с test_ — иначе pytest её не найдёт
# Имя файла тоже должно начинаться с test_ (или заканчиваться на _test)
def test_load_empty(tmp_path: Path):
    s = Storage(tmp_path / "tasks.json")
    # assert — ключевое слово Python. Если условие False — тест падает.
    # Оператор / у Path создаёт путь: tmp_path / "tasks.json" = <tmp>/tasks.json
    assert s.load() == []

def test_save_and_load(tmp_path: Path):
    s = Storage(tmp_path / "tasks.json")
    tasks = [
        Task(id=1, title="test"),
        Task(id=2, title="other", done=True),
    ]
    s.save(tasks)
    loaded = s.load()
    # Сравниваем списки целиком. Работает благодаря тому, что @dataclass автоматически создаёт метод __eq__
    assert loaded == tasks

def test_load_broken_json(tmp_path: Path):
    path = tmp_path / "tasks.json"
    path.write_text("{это не JSON", encoding="utf-8")  # портим файл
    s = Storage(path)
    assert s.load() == []