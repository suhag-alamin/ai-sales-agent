from app.modules.catalog.repositories import SORTS, ProductRepository
from app.modules.catalog.schemas import ProductCreate, ProductRead, ProductUpdate, ProductFilters, Page
from app.core.exceptions.errors import ConflictError, NotFoundError
from app.modules.catalog.models import Product


def to_read(product: Product) -> ProductRead:
    return ProductRead.model_validate(obj=product)


class ProductService:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    async def create_product(self, data: ProductCreate) -> ProductRead:
        if await self.repo.exists_by_slug(data.slug):
            raise ConflictError("product", data.slug)

        product = await self.repo.add(Product(**data.model_dump()))
        return to_read(product)

    async def get_all_products(self, filters: ProductFilters) -> Page:
        if (
            filters.min_price
            and filters.max_price
            and filters.min_price > filters.max_price
        ):
            filters.min_price, filters.max_price = filters.max_price, filters.min_price

        items, total = await self.repo.search(filters)

        return Page(
            items=[to_read(product) for product in items],
            total=total,
            page=filters.page,
            page_size=filters.page_sizeff,
        )

    async def get_product(self, slug: str) -> ProductRead:
        product = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError("product", slug)

        return to_read(product)

    async def update_product(self, slug: str, data: ProductUpdate) -> ProductRead:
        product = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError("product", slug)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        product = await self.repo.save(product)
        return to_read(product)

    async def archive_product(self, slug: str) -> None:
        product = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError("product", slug)

        product.is_active = False
