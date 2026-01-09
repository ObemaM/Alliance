from .country import Country
from .color import Color
from .category import Category
from .material import Material
from .product import Product
from .site_content import SiteContent
from .attribute import Attribute
from .product_attribute import ProductAttribute
from .product_image import ProductImage
from .order import Order
from .order_item import OrderItem

# __all__ - для импорта всех моделей, выше импортируем их все
__all__ = [
    "Country",
    "Color",
    "Category",
    "Material",
    "Product",
    "SiteContent",
    "Attribute",
    "ProductAttribute",
    "ProductImage",
    "Order",
    "OrderItem",
]