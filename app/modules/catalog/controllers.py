from app.modules.catalog.dependencies import ProductServiceDep
from app.modules.catalog.schemas import ProductCreate, ProductRead, ProductUpdate
from fastapi import APIRouter, Depends, status


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: ProductServiceDep
) -> ProductRead:
    return await service.create_product(data)
