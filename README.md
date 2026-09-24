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
python main.py --done
python main.py --pending
```

## Tests

```bash
pytest -v
```
## Итог:
<img width="1485" height="932" alt="в реадми" src="https://github.com/user-attachments/assets/5a4caf20-5eac-42df-8e6d-cce5b9272dde" />
