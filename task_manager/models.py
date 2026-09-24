# asdict — превращает dataclass-объект в обычный словарь (нужно для JSON)
# field — позволяет задать значение по умолчанию через функцию
from dataclasses import dataclass, asdict, field
from datetime import datetime

@dataclass # @dataclass автоматически создаёт __init__, __repr__ и __eq__ для класса
class Task:
    id: int
    title: str
    done: bool = False
    # default_factory — вызывается каждый раз при создании объекта
    # ВАЖНО: нельзя написать просто `created_at: str = datetime.now().isoformat()`,
    # потому что тогда время вычислилось бы один раз при импорте модуля
    # и было бы одинаковым у всех задач. default_factory решает эту проблему
    # isoformat(timespec="seconds") даёт строку вида "2025-01-15T14:30:00"
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)