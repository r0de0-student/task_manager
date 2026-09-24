import argparse # argparse — встроенный модуль для разбора аргументов командной строки
import sys # sys нужен для sys.exit() и sys.stderr — потока вывода ошибок
# Импорт из нашего пакета. Работает, только если запускаем из корня проекта, где лежит папка task_manager
from task_manager.cli import TaskManager
from task_manager.storage import Storage

def build_parser() -> argparse.ArgumentParser:
    # prog="task" — как программа будет называться в справке
    parser = argparse.ArgumentParser(prog="task", description="Менеджер задач")
    # add_subparsers создаёт подкоманды: task add, task list, task done, task delete
    # dest="command" — в args.command попадёт имя подкоманды ("add", "list", ...)
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="Добавить задачу")
    p_add.add_argument("title", help="Текст задачи")
    sub.add_parser("list", help="Показать задачи")
    p_done = sub.add_parser("done", help="Отметить выполненной")
    p_done.add_argument("id", type=int)
    p_del = sub.add_parser("delete", help="Удалить задачу")
    p_del.add_argument("id", type=int)
    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args() # parse_args() читает sys.argv (аргументы командной строки) и возвращает объект с полями: command, title, id
    # Создаём менеджер с хранилищем по умолчанию
    tm = TaskManager(Storage())
    try:
        # Можно было бы и через if/elif, но match читается чище
        if args.command == "add":
            task = tm.add(args.title)
            print(f"Добавлено: [{task.id}] {task.title}")
        elif args.command == "list":
            tasks = tm.list()
            if not tasks:
                print("Список пуст")
                return 0
            for t in tasks:
                # Тернарный оператор: mark = "x", если done, иначе " "
                mark = "x" if t.done else " "
                print(f"[{mark}] {t.id}. {t.title}")
        elif args.command == "done":
            task = tm.done(args.id)
            print(f"Выполнено: [{task.id}] {task.title}")
        elif args.command == "delete":
            tm.delete(args.id)
            print(f"Удалено: id={args.id}")
    except ValueError as e:
        # Ловим только ValueError — то, что мы сами бросаем в TaskManager
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    return 0
# Стандартная конструкция. Если файл запущен напрямую — выполняется main()
# Если импортирован из другого файла — не выполняется
if __name__ == "__main__":
    # sys.exit передаёт код возврата операционной системе
    sys.exit(main())