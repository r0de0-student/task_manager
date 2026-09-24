# pytest импортируем целиком — нужен для pytest.raises и @pytest.fixture
import pytest
from task_manager.cli import TaskManager
from task_manager.storage import Storage
# @pytest.fixture — это "заготовка" для теста. Убирает дублирование кода
@pytest.fixture
def tm(tmp_path):
    return TaskManager(Storage(tmp_path / "tasks.json"))

def test_add_and_list(tm):
    tm.add("first")
    tm.add("second")
    tasks = tm.list()
    # Списковые включения: достаём только заголовки и только id
    assert [t.title for t in tasks] == ["first", "second"]
    assert [t.id for t in tasks] == [1, 2]

def test_done(tm):
    tm.add("first")
    t = tm.done(1)
    # Проверяем, что флаг done стал True
    assert t.done is True
    # И что он сохранился на "диск"
    assert tm.list()[0].done is True

def test_done_missing(tm):
    with pytest.raises(ValueError):
        tm.done(999)

def test_delete(tm):
    tm.add("first")
    tm.delete(1)
    assert tm.list() == []

def test_delete_missing(tm):
    with pytest.raises(ValueError):
        tm.delete(999)

def test_filter(tm):
# filter(True) возвращает только выполненные,
# filter(False) — только активные
    tm.add("first")
    tm.add("second")
    tm.add("third")
    tm.done(2)  # отмечаем "second" выполненной
    done_tasks = tm.filter(True)
    pending_tasks = tm.filter(False)
    assert [t.title for t in done_tasks] == ["second"]
    assert [t.title for t in pending_tasks] == ["first", "third"]