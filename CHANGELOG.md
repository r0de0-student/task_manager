# Changelog
Все значимые изменения проекта фиксируются здесь.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/lang/ru/).

# Релиз 
## v[1.0.0] - 2026-09-25


## Добавлено
- Команды `add`, `list`, `done`, `delete`
- Приоритеты задач: `low`, `medium`, `high`
- Дедлайны в формате `YYYY-MM-DD` с автодетектом просрочки
- Фильтры `--done`, `--pending`, `--overdue`
- Сортировка по просрочке и приоритету (`--sort`)
- Сохранение данных в JSON
- Красивый вывод через библиотеку `rich` (таблицы, цвета, иконки)
- 16 тестов на pytest
- CI/CD на GitHub Actions (Python 3.11, 3.12, 3.13)