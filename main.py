import argparse
import sys
from datetime import date, datetime

from task_manager.cli import TaskManager
from task_manager.models import Priority
from task_manager.storage import Storage


def parse_date(s: str) -> date:
    # Кастомный валидатор для argparse. Принимает строку,
    # возвращает объект date. Если строка не в формате — argparse
    # поймает ошибку и покажет пользователю понятное сообщение.
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        # argparse ждёт, что мы поднимем ArgumentTypeError, чтобы показать
        # это сообщение пользователю.
        raise argparse.ArgumentTypeError(
            f"Неверный формат даты: '{s}'. Ожидается YYYY-MM-DD, например 2025-12-31"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="task", description="Менеджер задач")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Добавить задачу")
    p_add.add_argument("title", help="Текст задачи")
    p_add.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Приоритет задачи (по умолчанию medium)",
    )
    # --due принимает строку, но argparse преобразует её через нашу функцию parse_date.
    # type=parse_date — argparse вызовет parse_date(s) и подставит результат.
    p_add.add_argument(
        "--due", "-d",
        type=parse_date,
        default=None,
        help="Дедлайн в формате YYYY-MM-DD (например, 2025-12-31)",
    )

    p_list = sub.add_parser("list", help="Показать задачи")
    group = p_list.add_mutually_exclusive_group()
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
    group.add_argument(
        "--overdue",
        dest="filter",
        action="store_const",
        const="overdue",
        help="Показать только просроченные задачи",
    )
    p_list.add_argument(
        "--sort", "-s",
        action="store_true",
        help="Сортировать: просроченные → по приоритету",
    )

    p_done = sub.add_parser("done", help="Отметить выполненной")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Удалить задачу")
    p_del.add_argument("id", type=int)

    return parser


PRIORITY_MARKERS = {
    Priority.HIGH: "!!!",
    Priority.MEDIUM: "!  ",
    Priority.LOW: ".  ",
}


def format_due(t) -> str:
    # Возвращает строку с дедлайном для вывода в списке.
    # Если дедлайна нет — пустая строка.
    if t.due is None:
        return ""
    if t.is_overdue():
        return f"  ⚠ ПРОСРОЧЕНО ({t.due})"
    return f"  → до {t.due}"


def print_tasks(tasks) -> None:
    if not tasks:
        print("Список пуст")
        return
    for t in tasks:
        mark = "x" if t.done else " "
        marker = PRIORITY_MARKERS[t.priority]
        line = f"[{mark}] {marker} {t.id}. {t.title}  ({t.priority.value}, {t.created_at})"
        line += format_due(t)
        print(line)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    tm = TaskManager(Storage())

    try:
        if args.command == "add":
            priority = Priority(args.priority)
            task = tm.add(args.title, priority=priority, due=args.due)
            info = f"Добавлено: [{task.id}] {task.title} (приоритет: {task.priority.value}"
            if task.due:
                info += f", дедлайн: {task.due}"
            info += ")"
            print(info)

        elif args.command == "list":
            # args.filter может быть:
            #   None      -> показать всё
            #   True      -> --done
            #   False     -> --pending
            #   "overdue" -> --overdue
            if args.filter is None:
                tasks = tm.list()
            elif args.filter == "overdue":
                tasks = tm.filter_overdue()
            else:
                tasks = tm.filter(args.filter)

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
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())