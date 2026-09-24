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
- **Красивый вывод**: цветные таблицы, иконки приоритетов, зачёркнутые выполненные задачи

## Стек

- Python 3.11+
- Стандартные библиотеки: `argparse`, `json`, `pathlib`, `dataclasses`, `datetime`, `enum`
- [`rich`](https://github.com/Textualize/rich) — красивый вывод в терминале
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

### Установка как пакета
Проект можно установить как CLI-утилиту и вызывать командой `task`:
```bash
pip install -e ".[dev]"
task add "Купить молоко" -p high
task list --sort
# Команды
```

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
<img width="746" height="904" alt="2026-09-24_22-21-43" src="https://github.com/user-attachments/assets/80a421ea-1631-45b2-819f-79543e3f1fd0" />



