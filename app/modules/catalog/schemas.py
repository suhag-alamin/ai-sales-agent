from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any
from decimal import Decimal
from app.modules.catalog.models import Category
import uuid
from enum import Enum


class ProductBase(BaseModel):
    name: str = Field(..., title="Product Name", min_length=2, max_length=255)
    description: Optional[str] = Field(
        None, title="Product Description", max_length=1000)
    brand: str = Field(..., title="Product Brand",
                       min_length=2, max_length=255)
    category: Category = Field(..., title="Product Category")
    price: Decimal = Field(..., title="Product Price",
                           gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(..., title="Product Stock", ge=0)
    warranty_months: int = Field(
        12, title="Warranty Period in Months", ge=0)
    specs: dict[str, Any] = Field(
        default_factory=dict, title="Product Specifications")


class ProductCreate(ProductBase):
    slug: str = Field(..., title="Product Slug", min_length=2, max_length=255)


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., title="Product ID")
    slug: str = Field(..., title="Product Slug")
    in_stock: bool = Field(..., title="Is Product In Stock")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None, title="Product Name", min_length=2, max_length=255)
    description: Optional[str] = Field(
        None, title="Product Description", max_length=1000)
    brand: Optional[str] = Field(None, title="Product Brand",
                                 min_length=2, max_length=255)
    category: Optional[Category] = Field(None, title="Product Category")
    price: Optional[Decimal] = Field(None, title="Product Price",
                                     gt=0, max_digits=10, decimal_places=2)
    stock: Optional[int] = Field(None, title="Product Stock", ge=0)
    warranty_months: Optional[int] = Field(
        None, title="Warranty Period in Months", ge=0)
    specs: Optional[dict[str, Any]] = Field(
        default=None, title="Product Specifications")


class SortOption(str, Enum):
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    NAME = "name"


class ProductFilters(BaseModel):
    q: str | None = Field(None, title="Search Query",
                          min_length=2, max_length=255)
    category: Category | None = Field(None, title="Product Category")
    brand: str | None = Field(
        None, title="Product Brand", min_length=2, max_length=255)
    min_price: Decimal | None = Field(None, title="Minimum Price", gt=0)
    max_price: Decimal | None = Field(None, title="Maximum Price", gt=0)
    in_stock: bool | None = Field(None, title="In Stock Only")
    sort: SortOption = Field(SortOption.NEWEST, title="Sort Option")
    page: int = Field(1, title="Page Number", ge=1)
    page_size: int = Field(10, title="Page Size", ge=1, le=500)


class Page(BaseModel):
    items: list[ProductRead] = Field(title="List of Products")
    total: int = Field(title="Total Number of Products")
    page: int = Field(title="Current Page Number")
    page_size: int = Field(title="Number of Products per Page")
