<div align="center">

  ![Tests](https://github.com/r0de0-student/task_manager/actions/workflows/tests.yml/badge.svg)
  ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![JSON](https://img.shields.io/badge/JSON-storage-000000?style=for-the-badge&logo=json&logoColor=white)
  ![pytest](https://img.shields.io/badge/pytest-16_passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

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
- **Красивый вывод**: цветные таблицы, иконки приоритетов, зачёркнутые выполненные задачи
- **Тесты** на pytest (16 тестов)
- **CI/CD**: автотесты на GitHub Actions для Python 3.11, 3.12, 3.13

## Стек

- Python 3.11+
- Стандартные библиотеки: `argparse`, `json`, `pathlib`, `dataclasses`, `datetime`, `enum`
- [`rich`](https://github.com/Textualize/rich) — красивый вывод в терминале
- `pytest` для тестов
- GitHub Actions для CI

## Установка и запуск

```bash
git clone https://github.com/r0de0-student/task_manager.git
cd task_manager
python -m venv .venv
# Windows:
.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Установка как CLI-утилиты
Проект можно установить в editable-режиме и вызывать командой task из любой папки (пока активировано виртуальное окружение):

```bash
pip install -e ".[dev]"
task add "Купить молоко" -p high
task list --sort
task done 1
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

# Демонстрация

<img width="746" height="904" alt="2026-09-24_22-21-43" src="https://github.com/user-attachments/assets/80a421ea-1631-45b2-819f-79543e3f1fd0" />

## Структура проекта
```bash
task_manager/
├── .github/
│   └── workflows/
│       └── tests.yml       # CI: автотесты при push
├── task_manager/           # пакет с логикой
│   ├── __init__.py
│   ├── models.py           # модель Task, Priority, проверка просрочки
│   ├── storage.py          # чтение/запись JSON
│   └── cli.py              # бизнес-логика команд
├── tests/                  # тесты pytest
│   ├── test_cli.py
│   └── test_storage.py
├── main.py                 # точка входа, CLI через argparse
├── conftest.py             # конфигурация pytest
├── pyproject.toml          # метаданные пакета и зависимости
├── requirements.txt        # зависимости для быстрой установки
├── CHANGELOG.md            # история версий
├── LICENSE                 # MIT
├── NOTES.md                # Мои пометки
└── README.md

```

## Разработка
```bash
# Клонировать
git clone https://github.com/r0de0-student/task_manager.git
cd task_manager
# Виртуальное окружение
python -m venv .venv
.venv\Scripts\activate.bat  # Windows
# Установить с dev-зависимостями
pip install -e ".[dev]"
# Прогнать тесты
pytest -v
```

# Лицензия
MIT — см. файл LICENSE.

# Changelog
Историю изменений см. в CHANGELOG.md.

# Обратная связь

Проект сделан в учебных целях, но я старался сделать его максимально приближенным к реальному production-коду.

Буду рад:
- ⭐ Если понравился проект — поставь звезду.
- 🐛 Если нашёл баг — открой [issue](https://github.com/r0de0-student/task_manager/issues).
- 💡 Если есть идеи — пиши в [discussions](https://github.com/r0de0-student/task_manager/discussions) или создавай pull request.

Спасибо, что заглянул!
