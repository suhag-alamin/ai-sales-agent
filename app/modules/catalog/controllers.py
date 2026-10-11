from app.modules.catalog.dependencies import ProductServiceDep
from app.modules.catalog.schemas import ProductCreate, ProductFilters, ProductRead, ProductUpdate, Page
from fastapi import APIRouter, Depends, Query, status
from typing import Annotated

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    service: ProductServiceDep
) -> ProductRead:
    return await service.create_product(data)


@router.get("/", response_model=Page)
async def get_all_products(
    filters: Annotated[ProductFilters, Query()],
    service: ProductServiceDep
) -> Page:
    return await service.get_all_products(filters)


@router.get("/{slug}", response_model=ProductRead)
async def get_product(
    slug: str,
    service: ProductServiceDep
) -> ProductRead:
    return await service.get_product(slug)


@router.patch("/{slug}", response_model=ProductRead)
async def update_product(
    slug: str,
    data: ProductUpdate,
    service: ProductServiceDep
) -> ProductRead:
    return await service.update_product(slug, data)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_product(
    slug: str,
    service: ProductServiceDep
) -> None:
    await service.archive_product(slug)
