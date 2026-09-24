# asdict — превращает dataclass-объект в обычный словарь (нужно для JSON)
# field — позволяет задать значение по умолчанию через функцию
# Enum — перечисление. Позволяет ограничить значения конкретным списком
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Словарь для сортировки: чем больше число, тем выше приоритет
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
    # Приоритет по умолчанию — MEDIUM. Обрати внимание: поля со значениями по умолчанию
    # идут ПОСЛЕ полей без таковых, иначе Python ругается.
    priority: Priority = Priority.MEDIUM
    # default_factory — вызывается каждый раз при создании объекта
    # ВАЖНО: нельзя написать просто `created_at: str = datetime.now().isoformat()`,
    # потому что тогда время вычислилось бы один раз при импорте модуля
    # и было бы одинаковым у всех задач. default_factory решает эту проблему
    # isoformat(timespec="seconds") даёт строку вида "2025-01-15T14:30:00"
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict:
        d = asdict(self)
        # asdict превращает Enum в строку уже сам (благодаря наследованию от str),
        # но на всякий случай оставим явное преобразование — так надёжнее.
        d["priority"] = self.priority.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        # Если в старом JSON нет поля priority — подставим MEDIUM.
        # Это важно: пользователи со старыми файлами не должны страдать.
        if "priority" in data:
            data["priority"] = Priority(data["priority"])
        else:
            data["priority"] = Priority.MEDIUM
        return cls(**data)