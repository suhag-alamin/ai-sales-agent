from app.db.session import SessionDep
from app.modules.catalog.repositories import ProductRepository
from typing import Annotated
from fastapi import Depends
from app.modules.catalog.services import ProductService


def get_product_repository(session: SessionDep) -> ProductRepository:
    return ProductRepository(session)


ProductRepositoryDep = Annotated[ProductRepository, Depends(
    get_product_repository, scope="function")]


def get_product_service(repo: ProductRepositoryDep) -> ProductService:
    return ProductService(repo)


ProductServiceDep = Annotated[ProductService, Depends(
    get_product_service, scope="function")]
