from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass
from flask_login import UserMixin
from . import db, bcrypt


class User(db.Model, UserMixin, MappedAsDataclass):
    def __post_init__(self):
        print("running")
        self.set_password(self.password)  # type: ignore
        print(self.password)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(
        repr=False,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
    )
    todos: Mapped[list["Todo"]] = relationship(
        back_populates="user", cascade="all,delete-orphan", init=False
    )

    image: Mapped[str] = mapped_column(
        default="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp",
        nullable=True,
    )

    def set_password(self, password) -> None:
        self.password = bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")  # type: ignore

    def is_valid_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password, password)


class Todo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    user: Mapped["User"] = relationship(back_populates="todos", init=False, repr=False)
    done:Mapped[bool] = mapped_column(default=False,nullable=True)
