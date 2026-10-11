import enum
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimeStampMixin
from sqlalchemy import Boolean, CheckConstraint, Integer, String, Numeric, Text, Enum
from sqlalchemy.dialects.postgresql import JSONB
from typing import Any


class Category(str, enum.Enum):
    PHONE = "phone"
    LAPTOP = "laptop"
    TABLET = "tablet"
    ACCESSORY = "accessory"


class Product(Base, TimeStampMixin):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, unique=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    brand: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    description: Mapped[str] = mapped_column(
        Text, default="", server_default="", nullable=True)
    specs: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}")
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true")
    warranty_months: Mapped[int] = mapped_column(
        Integer, default=12, server_default="12")

    category: Mapped[Category] = mapped_column(
        Enum(Category, native_enum=False, length=50, values__callable=lambda e: [v.value for v in e],), nullable=False, index=True
    )

    @property
    def in_stock(self) -> bool:
        return self.stock > 0
