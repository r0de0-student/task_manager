import argparse
import sys
from datetime import datetime

# Импорты из rich — библиотека для красивого вывода в терминале.
# Console — основной объект для вывода. Он сам определяет, поддерживает ли
# терминал цвета (Windows Terminal — да, старый cmd — не всегда).
# Table — рисует красивые таблицы с рамками и выравниванием.
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from task_manager.cli import TaskManager
from task_manager.models import Priority
from task_manager.storage import Storage

# Создаём глобальный console — через него будем выводить всё красиво.
# Один экземпляр на всю программу — так рекомендуют авторы rich.
console = Console()


def parse_date(s: str):
    # Кастомный валидатор для argparse. Принимает строку, возвращает date.
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Неверный формат даты: '{s}'. Ожидается YYYY-MM-DD, например 2026-12-31"
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
    p_add.add_argument(
        "--due", "-d",
        type=parse_date,
        default=None,
        help="Дедлайн в формате YYYY-MM-DD (например, 2026-12-31)",
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


# Стили rich — именованные цвета и модификаторы.
# Можно использовать цвета по имени (red, green, yellow) или по hex (#ff0000).
# Из модификаторов: bold, italic, underline, dim.
PRIORITY_STYLES = {
    Priority.HIGH: "bold red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "dim",
}

PRIORITY_ICONS = {
    Priority.HIGH: "🔴",
    Priority.MEDIUM: "🟡",
    Priority.LOW: "🟢",
}


def make_due_cell(t) -> str:
    # Возвращает строку с дедлайном для ячейки таблицы.
    # Мы возвращаем markdown-подобную разметку rich — [red]...[/red],
    # rich сам её распарсит и покрасит.
    if t.due is None:
        return "[dim]—[/dim]"
    if t.is_overdue():
        return f"[bold red]⚠ {t.due}[/bold red]"
    return f"[green]{t.due}[/green]"


def print_tasks(tasks) -> None:
    # Если список пуст — показываем панель вместо таблицы.
    if not tasks:
        console.print(Panel("Список пуст", style="dim", expand=False))
        return

    # Table — объект таблицы. title и show_lines делают её наряднее.
    table = Table(
        title=f"Задачи ({len(tasks)})",
        show_header=True,
        header_style="bold cyan",
        show_lines=False,
    )

    # Колонки. У каждой — имя, стиль (применяется ко всем ячейкам),
    # justify (выравнивание), no_wrap (запрет переноса), width (ширина).
    table.add_column("✓", justify="center", width=3)
    table.add_column("Приоритет", justify="center", width=10)
    table.add_column("ID", justify="right", width=4, style="dim")
    table.add_column("Задача", style="white", no_wrap=False)
    table.add_column("Дедлайн", justify="left", width=14)
    table.add_column("Создана", style="dim", width=20)

    for t in tasks:
        # Статус: зелёная галочка для выполненных, пустой кружок для активных.
        # rich понимает эмодзи и юникод-символы.
        status = "[green]✓[/green]" if t.done else "[ ]"

        # Приоритет — цветной маркер.
        priority = f"{PRIORITY_ICONS[t.priority]} {t.priority.value}"
        priority_styled = f"[{PRIORITY_STYLES[t.priority]}]{priority}[/{PRIORITY_STYLES[t.priority]}]"

        # Стиль заголовка: выполненные задачи — зачёркнуты и потускневшие.
        title_text = f"[strike dim]{t.title}[/strike dim]" if t.done else t.title

        # add_row добавляет строку в таблицу. Значения идут в порядке колонок.
        table.add_row(
            status,
            priority_styled,
            str(t.id),
            title_text,
            make_due_cell(t),
            t.created_at.replace("T", " "),
        )

    console.print(table)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    tm = TaskManager(Storage())

    try:
        if args.command == "add":
            priority = Priority(args.priority)
            task = tm.add(args.title, priority=priority, due=args.due)

            # Панель для сообщения об успехе. expand=False — панель по ширине текста.
            info = f"Задача [bold]#{task.id}[/bold] добавлена: [cyan]{task.title}[/cyan]"
            info += f"\nПриоритет: {PRIORITY_ICONS[task.priority]} [bold]{task.priority.value}[/bold]"
            if task.due:
                info += f"\nДедлайн: [green]{task.due}[/green]"
            console.print(Panel(info, title="[green]✓ Успех[/green]", border_style="green", expand=False))

        elif args.command == "list":
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
            console.print(f"[green]✓[/green] Выполнено: [strike dim]{task.title}[/strike dim]")

        elif args.command == "delete":
            tm.delete(args.id)
            console.print(f"[red]✗[/red] Удалено: id={args.id}")

    except ValueError as e:
        # Ошибки выводим через console в красной панели — заметнее.
        console.print(Panel(f"[red]{e}[/red]", title="[red]Ошибка[/red]", border_style="red", expand=False))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())