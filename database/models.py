from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///db/database.db")
async_session = async_sessionmaker(engine, expire_on_commit=True)


class Base(DeclarativeBase):
    pass


class UserPreInfo(Base):
    __tablename__ = "profile2"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str | None] = mapped_column(nullable=True)
    fio: Mapped[str | None] = mapped_column(nullable=True)
    photo: Mapped[str | None] = mapped_column(nullable=True)
    geo_position: Mapped[str | None] = mapped_column(nullable=True)
    soglas : Mapped[str]
    tg_data: Mapped[str | None] = mapped_column(nullable=True)
    photo_URL: Mapped[str | None] = mapped_column(nullable=True)



class UserInfo(Base):
    __tablename__ = "profile3"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str | None] = mapped_column(nullable=True)
    fio: Mapped[str | None] = mapped_column(nullable=True)
    photo: Mapped[str | None] = mapped_column(nullable=True)
    geo_position: Mapped[str | None] = mapped_column(nullable=True)
    soglas : Mapped[str]
    tg_data: Mapped[str | None] = mapped_column(nullable=True)
    photo_URL: Mapped[str | None] = mapped_column(nullable=True)
    approval: Mapped[bool | None] = mapped_column(nullable=True)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)