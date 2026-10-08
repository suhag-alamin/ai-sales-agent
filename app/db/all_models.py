"""Import all the models, so that Base has them before being imported by Alembic."""
from app.modules.users.models import User
from app.modules.catalog.models import Product, Category
