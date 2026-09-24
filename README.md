# Task Manager CLI

Простой менеджер задач для командной строки на Python.

## Возможности

- Добавление, просмотр, отметка выполненных и удаление задач
- Сохранение данных в JSON-файл
- Тесты на pytest (8 тестов)

## Стек

- Python 3.14+
- Стандартные библиотеки: `argparse`, `json`, `pathlib`, `dataclasses`
- `pytest` для тестов

## Установка и запуск

```bash
git clone https://github.com/r0de0-student/task_manager.git
cd task_manager
python -m venv .venv 
.venv\Scripts\activate.bat 
pip install -r requirements.txt
```

## Примеры использования

```bash
python main.py add "Купить молоко"
python main.py list
python main.py done 1
python main.py delete 1
python main.py --help
```

## Tests

```bash
pytest -v
```