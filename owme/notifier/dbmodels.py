from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


association_table = Table(
    'apartment_notification_associations_table',
    Base.metadata,
    Column('apartment_id', ForeignKey('apartments.id'), primary_key=True),
    Column('notification_id', ForeignKey('notifications.id'), primary_key=True),
)


class Apartment(Base):
    __tablename__ = 'apartments'

    url: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    number: Mapped[int]
    price: Mapped[Decimal]
    available: Mapped[bool]
    last_availability_change: Mapped[datetime] = mapped_column(insert_default=func.now())

    notifications: Mapped[list[Notification]] = relationship(secondary=association_table, back_populates='apartments')

    def __str__(self) -> str:
        return f'{self.name} -  €{self.price:.2f}: {self.url}'

    @property
    def name(self) -> str:
        return f'{self.address} Studio {self.number}'


class Notification(Base):
    __tablename__ = 'notifications'

    email: Mapped[str]
    apartments: Mapped[list[Apartment]] = relationship(secondary=association_table, back_populates='notifications')
    sent_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    subject: Mapped[str]
    body: Mapped[str]
