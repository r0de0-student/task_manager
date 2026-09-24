<div align="center">

  ![Tests](https://github.com/r0de0-student/task_manager/actions/workflows/tests.yml/badge.svg)
  ![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![JSON](https://img.shields.io/badge/JSON-storage-000000?style=for-the-badge&logo=json&logoColor=white)
  ![pytest](https://img.shields.io/badge/pytest-16_passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)

</div>

# Task Manager CLI

Простой менеджер задач для командной строки на Python.

## Возможности

- **Задачи**: добавление, просмотр, отметка выполненных, удаление
- **Приоритеты**: `low` / `medium` / `high` с сортировкой
- **Дедлайны**: указание срока в формате `YYYY-MM-DD`, автоматическое определение просроченных задач
- **Фильтры**: показать только выполненные, только активные или только просроченные
- **Сортировка**: просроченные всплывают наверх, дальше по приоритету
- **Сохранение** данных в JSON-файл
- **Тесты** на pytest (16 тестов)
- **CI/CD**: автотесты на GitHub Actions для Python 3.11, 3.12, 3.13

## Стек

- Python 3.11+
- Стандартные библиотеки: `argparse`, `json`, `pathlib`, `dataclasses`, `datetime`, `enum`
- `pytest` для тестов
- GitHub Actions для CI

# Установка и запуск

```bash
git clone https://github.com/r0de0-student/task_manager.git
cd task_manager
python -m venv .venv
# Windows:
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Команды

## Добавить задачу
```bash
# Простая задача
python main.py add "Купить молоко"
# С приоритетом
python main.py add "Сдать отчёт" -p high
python main.py add "Почитать книгу" -p low
# С дедлайном (формат YYYY-MM-DD)
python main.py add "Оплатить счета" --due 2026-12-31
# Всё вместе
python main.py add "Подготовить презентацию" -p high --due 2026-10-15
```

## Показать задачи
```bash
# Все задачи
python main.py list
# Только выполненные
python main.py list --done
# Только активные (невыполненные)
python main.py list --pending
# Только просроченные
python main.py list --overdue
# Отсортировать: просроченные → по приоритету
python main.py list --sort
# Комбинировать: активные, отсортированные по приоритету
python main.py list --pending --sort
```

## Отметить выполненной / удалить
```bash
python main.py done 1
python main.py delete 2
```

## Справка
```bash
python main.py --help
python main.py add --help
python main.py list --help
```

## Тесты
```bash
pytest -v
```

# Пример вывода
```bash
$ python main.py list --sort
[ ] .   3. Просроченная задача  (low, 2026-09-24T18:09:42)  ⚠ ПРОСРОЧЕНО (2020-01-01)
[ ] !!! 1. Сдать отчёт          (high, 2026-09-24T18:09:30)  ⚠ ПРОСРОЧЕНО (2025-12-31)
[ ] !   2. Помыть посуду        (medium, 2026-09-24T18:09:37)
[ ] !!! 4. Оплатить счета       (high, 2026-09-24T18:12:01)  → до 2026-12-31
```

# Демонстрация
<img width="941" height="799" alt="Снимок экрана 2026-09-24 181058" src="https://github.com/user-attachments/assets/425bd7e2-74eb-4eff-ac87-955c8cb99c0a" />


