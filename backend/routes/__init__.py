from .countries import router as countries_router
from .colors import router as colors_router
from .categories import router as categories_router
from .materials import router as materials_router
from .products import router as products_router
from .site_content import router as site_content_router
from .product_images import router as product_images_router
from .product_attributes import router as product_attributes_router
from .order_items import router as order_items_router
from .attributes import router as attributes_router
from .orders import router as orders_router

__all__ = [
    "countries_router",
    "colors_router",
    "categories_router",
    "materials_router",
    "products_router",
    "site_content_router",
    "product_images_router",
    "product_attributes_router",
    "order_items_router",
    "attributes_router",
    "orders_router",
]
