import argparse # argparse — встроенный модуль для разбора аргументов командной строки
import sys # sys нужен для sys.exit() и sys.stderr — потока вывода ошибок
# Импорт из нашего пакета. Работает, только если запускаем из корня проекта, где лежит папка task_manager
from task_manager.cli import TaskManager
# Дополнительно импортируем Priority — нужен для преобразования строки в Enum.
from task_manager.models import Priority
from task_manager.storage import Storage

def build_parser() -> argparse.ArgumentParser:
    # prog="task" — как программа будет называться в справке
    parser = argparse.ArgumentParser(prog="task", description="Менеджер задач")
    # add_subparsers создаёт подкоманды: task add, task list, task done, task delete
    # dest="command" — в args.command попадёт имя подкоманды ("add", "list", ...)
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="Добавить задачу")
    p_add.add_argument("title", help="Текст задачи")
    # choices ограничивает допустимые значения. argparse сам проверит,
    # что пользователь ввёл одно из: low, medium, high.
    # "-p" — короткий псевдоним, можно писать `-p high` вместо `--priority high`.
    p_add.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Приоритет задачи (по умолчанию medium)",
    )
    p_list = sub.add_parser("list", help="Показать задачи")
    # Если пользователь напишет `list --done --pending`, будет ошибка.
    group = p_list.add_mutually_exclusive_group()
    # action="store_const" — при указании флага в переменную filter запишется
    # константа (True или False), а не строка
    group.add_argument(
        "--done",
        dest="filter",
        action="store_const",
        const=True,
        help="Показать только выполненные задачи",
    )
    group.add_argument(
        "--pending",
        dest="filter",
        action="store_const",
        const=False,
        help="Показать только невыполненные задачи",
    )
    # Флаг сортировки. store_true значит "если указали — True, иначе False".
    p_list.add_argument(
        "--sort", "-s",
        action="store_true",
        help="Сортировать по приоритету (high → low)",
    )
    p_done = sub.add_parser("done", help="Отметить выполненной")
    p_done.add_argument("id", type=int)
    p_del = sub.add_parser("delete", help="Удалить задачу")
    p_del.add_argument("id", type=int)
    return parser


# Визуальные маркеры приоритета. Маленькие пометки вместо слов — компактнее.
PRIORITY_MARKERS = {
    Priority.HIGH: "!!!",
    Priority.MEDIUM: "!  ",
    Priority.LOW: ".  ",
}


def print_tasks(tasks) -> None:
    # Вынесли вывод списка в отдельную функцию — переиспользуем в main().
    if not tasks:
        print("Список пуст")
        return
    for t in tasks:
        # Тернарный оператор: mark = "x", если done, иначе " "
        mark = "x" if t.done else " "
        marker = PRIORITY_MARKERS[t.priority]
        print(f"[{mark}] {marker} {t.id}. {t.title}  ({t.priority.value}, {t.created_at})")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args() # parse_args() читает sys.argv (аргументы командной строки) и возвращает объект с полями: command, title, id
    # Создаём менеджер с хранилищем по умолчанию
    tm = TaskManager(Storage())
    try:
        # Можно было бы и через if/elif, но match читается чище
        if args.command == "add":
            # Преобразуем строку "high" в объект Priority.HIGH.
            priority = Priority(args.priority)
            task = tm.add(args.title, priority=priority)
            print(f"Добавлено: [{task.id}] {task.title} (приоритет: {task.priority.value})")
        elif args.command == "list":
            if args.filter is None:
                # args.filter может быть:
                #   None  -> пользователь не указал ничего -> показать всё
                #   True  -> указал --done
                #   False -> указал --pending
                tasks = tm.list()
            else:
                tasks = tm.filter(args.filter)
            # Если пользователь указал --sort — сортируем по приоритету.
            if args.sort:
                tasks = tm.sorted_by_priority(tasks)
            print_tasks(tasks)
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