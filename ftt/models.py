from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_active: Mapped[bool] = mapped_column(default=True)
