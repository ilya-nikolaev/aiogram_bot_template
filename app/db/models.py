from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN, TIMESTAMP
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from sqlalchemy import false
from sqlalchemy.sql.functions import now

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    username: Mapped[str] = mapped_column(TEXT, nullable=True, unique=True)

    banned: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=false())

    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=now())
