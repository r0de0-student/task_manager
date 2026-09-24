# asdict — превращает dataclass-объект в обычный словарь (нужно для JSON)
# field — позволяет задать значение по умолчанию через функцию
from dataclasses import dataclass, asdict, field
# datetime — встроенный модуль для работы с датой и временем
from datetime import datetime, date
# Optional — старый способ записать "может быть None".
# В Python 3.10+ есть более короткий: `date | None`.
from typing import Optional

# Enum — перечисление. Позволяет ограничить значения конкретным списком.
# Класс Priority.LOW — это уже не просто строка "low", а объект с именем и значением.
from enum import Enum


class Priority(str, Enum):
    # Наследуемся от str, чтобы значения вели себя как строки при JSON-сериализации:
    # json.dumps(Priority.HIGH) == '"high"' без дополнительных преобразований.
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Словарь для сортировки: чем больше число, тем выше приоритет.
PRIORITY_ORDER = {
    Priority.LOW: 1,
    Priority.MEDIUM: 2,
    Priority.HIGH: 3,
}


@dataclass # @dataclass автоматически создаёт __init__, __repr__ и __eq__ для класса
class Task:
    id: int
    title: str
    done: bool = False
    priority: Priority = Priority.MEDIUM
    # due — дедлайн задачи. Может быть None (значит, без дедлайна).
    # Тип date, а не datetime — нам важна только дата без времени.
    # Union[str, None] используется в типизации для "может быть строкой, а может быть None".
    due: Optional[date] = None
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["priority"] = self.priority.value
        # date нельзя напрямую превратить в JSON — нужен isoformat().
        # Если due = None — оставляем None (json.dumps превратит его в null).
        d["due"] = self.due.isoformat() if self.due else None
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        if "priority" in data:
            data["priority"] = Priority(data["priority"])
        else:
            data["priority"] = Priority.MEDIUM
        # Обратная совместимость: если в старом JSON нет due — ставим None.
        # Если есть — парсим ISO-строку обратно в объект date.
        if data.get("due"):
            # date.fromisoformat("2025-12-31") → date(2025, 12, 31)
            data["due"] = date.fromisoformat(data["due"])
        else:
            data["due"] = None
        return cls(**data)

    def is_overdue(self) -> bool:
        # Задача просрочена, если:
        #   1) у неё есть дедлайн
        #   2) она ещё не выполнена
        #   3) дедлайн уже прошёл (today больше due)
        if self.due is None:
            return False
        if self.done:
            return False
        return date.today() > self.due