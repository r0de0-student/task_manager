# pytest импортируем целиком — нужен для pytest.raises и @pytest.fixture
import pytest
# Импортируем date и timedelta — нужны для тестов с дедлайнами
from datetime import date, timedelta

from task_manager.cli import TaskManager
from task_manager.storage import Storage
from task_manager.models import Priority


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


def test_add_with_priority(tm):
    task = tm.add("важное", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH
    loaded = tm.list()[0]
    assert loaded.priority == Priority.HIGH


def test_sorted_by_priority(tm):
    tm.add("низкий", priority=Priority.LOW)
    tm.add("высокий", priority=Priority.HIGH)
    tm.add("средний", priority=Priority.MEDIUM)
    tasks = tm.sorted_by_priority()
    assert [t.title for t in tasks] == ["высокий", "средний", "низкий"]


# --- Новые тесты для дедлайнов ---


def test_add_with_due(tm):
    # Бертём завтрашнюю дату: сегодня + 1 день.
    # timedelta(days=1) — это "сдвиг на один день".
    tomorrow = date.today() + timedelta(days=1)
    task = tm.add("с дедлайном", due=tomorrow)

    # Проверяем, что дедлайн сохранился на объекте...
    assert task.due == tomorrow
    # ...и что он корректно читается из JSON обратно.
    loaded = tm.list()[0]
    assert loaded.due == tomorrow


def test_add_without_due(tm):
    # Задача без дедлайна: due должен быть None.
    task = tm.add("без дедлайна")
    assert task.due is None
    assert tm.list()[0].due is None


def test_is_overdue(tm):
    # Вчерашняя дата — точно просрочена.
    yesterday = date.today() - timedelta(days=1)
    # Завтрашняя — точно актуальна.
    tomorrow = date.today() + timedelta(days=1)

    tm.add("просроченная", due=yesterday)
    tm.add("актуальная", due=tomorrow)
    tm.add("без дедлайна")

    # Ожидаем только одну просроченную задачу.
    overdue = tm.filter_overdue()
    assert [t.title for t in overdue] == ["просроченная"]


def test_done_not_overdue(tm):
    # Выполненные задачи не считаются просроченными, даже если срок прошёл.
    yesterday = date.today() - timedelta(days=1)
    task = tm.add("просроченная, но выполненная", due=yesterday)
    tm.done(task.id)
    assert tm.filter_overdue() == []


def test_sort_overdue_first(tm):
    # Просроченные должны быть сверху, даже если у них низкий приоритет.
    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=1)

    tm.add("high без срока", priority=Priority.HIGH, due=tomorrow)
    tm.add("low просрочено", priority=Priority.LOW, due=yesterday)

    tasks = tm.sorted_by_priority()
    # Первой должна идти просроченная, несмотря на низкий приоритет.
    assert tasks[0].title == "low просрочено"
    assert tasks[1].title == "high без срока"