<div align="center">

  ![Tests](https://github.com/r0de0-student/task_manager/actions/workflows/tests.yml/badge.svg)
  ![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![JSON](https://img.shields.io/badge/JSON-storage-000000?style=for-the-badge&logo=json&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

# Task Manager CLI

Простой менеджер задач для командной строки на Python.

## Возможности

- Добавление, просмотр, отметка выполненных и удаление задач
- Сохранение данных в JSON-файл
- Тесты на pytest (11 тестов)

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
python main.py add "Купить молоко" -p high
python main.py add "Купить молоко" -p low
python main.py list
python main.py list --sort
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

## Добавление к проекту
<img width="1244" height="842" alt="image" src="https://github.com/user-attachments/assets/17dff621-1ed1-441d-a80b-f0b99b7684a6" />

