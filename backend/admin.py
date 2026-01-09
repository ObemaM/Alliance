from sqladmin import Admin, ModelView
from database import engine
from models import Product, Country, Color, Category, Material, SiteContent, ProductImage, OrderItem, ProductAttribute, Order, Attribute 

# Импортируем app из main
from main import app

# Создаем админку
admin = Admin(app, engine)

# Настройка для товаров
class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.quantity, Product.category_id]
    column_searchable_list = [Product.name, Product.description]
    column_sortable_list = [Product.price, Product.name]
    form_columns = [Product.name, Product.description, Product.price, Product.quantity, 
                   Product.category_id, Product.material_id, Product.country_id, Product.color_id]

# Настройка для контента сайта
class SiteContentAdmin(ModelView, model=SiteContent):
    column_list = [SiteContent.key, SiteContent.value, SiteContent.description]

# Настройка для простых моделей
class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id, Country.name]

class ColorAdmin(ModelView, model=Color):
    column_list = [Color.id, Color.name, Color.code]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.slug, Category.parent_id]

class MaterialAdmin(ModelView, model=Material):
    column_list = [Material.id, Material.name]

class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.id, ProductImage.product_id, ProductImage.url]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.customer_name, Order.customer_phone, Order.total_amount, Order.status]
    column_searchable_list = [Order.customer_name, Order.customer_phone]
    column_sortable_list = [Order.total_amount, Order.status]

class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [OrderItem.order_id, OrderItem.product_id, OrderItem.quantity, OrderItem.price_at_purchase]

class ProductAttributeAdmin(ModelView, model=ProductAttribute):
    column_list = [ProductAttribute.product_id, ProductAttribute.attribute_id, ProductAttribute.value_text]

class AttributeAdmin(ModelView, model=Attribute):
    column_list = [Attribute.id, Attribute.name]

# Регистрируем все модели
admin.add_view(ProductAdmin)
admin.add_view(CountryAdmin)
admin.add_view(ColorAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(MaterialAdmin)
admin.add_view(SiteContentAdmin)
admin.add_view(ProductImageAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(ProductAttributeAdmin)
admin.add_view(AttributeAdmin)