from sqladmin import Admin, ModelView
from pathlib import Path
from sqlalchemy import func, select
from wtforms import StringField
from wtforms.validators import Optional

from database import engine
from models import Product, Country, Color, Category, Material, SiteContent, ProductImage, OrderItem, ProductAttribute, Order, Attribute 

# Импортируем app из main
from main import app

# Создаем админку
admin = Admin(app, engine, templates_dir=str(Path(__file__).resolve().parent / "templates"), title="Панель администратора")

# Настройка для товаров
class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"
    column_list = [Product.id, Product.name, Product.price, Product.quantity, Product.pack_quantity, Product.category]
    column_searchable_list = [Product.name, Product.description]
    column_sortable_list = [Product.price, Product.quantity, Product.name]
    form_columns = [
        Product.name,
        Product.description,
        Product.price,
        Product.quantity,
        Product.pack_quantity,
        Product.weight,
        Product.category,
    ]
    column_labels = {
        Product.id: "ID",
        Product.name: "Название",
        Product.description: "Описание",
        Product.price: "Цена",
        Product.quantity: "Количество в наличии",
        Product.pack_quantity: "Количество в упаковке",
        Product.category_id: "Категория",
        Product.category: "Категория",
        Product.weight: "Вес",
        Product.material: "Материал",
        Product.country: "Страна",
        Product.color: "Цвет",
    }

    # Метод SQLAdmin для автоматического создания формы на основе модели SQLAlchemy
    async def scaffold_form(self, rules=None):
        form = await super().scaffold_form(rules)

        class ProductForm(form):
            country_name = StringField("Страна", validators=[Optional()], render_kw={"class": "form-control"})
            material_name = StringField("Материал", validators=[Optional()], render_kw={"class": "form-control"})
            color_name = StringField("Цвет", validators=[Optional()], render_kw={"class": "form-control"})
            category_name = StringField("Категория", validators=[Optional()], render_kw={"class": "form-control"})

        return ProductForm

    async def _get_or_create_by_name(self, ref_model, name: str) -> int:
        normalized = name.strip()
        async with self.session_maker(expire_on_commit=False) as session:
            stmt = select(ref_model).where(func.lower(ref_model.name) == normalized.lower())
            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj is not None:
                return obj.id

            obj = ref_model(name=normalized)
            session.add(obj)
            await session.flush()
            await session.commit()
            return obj.id

    async def on_model_change(self, data: dict, model, is_created: bool, request):
        country_name = (data.pop("country_name", None) or "").strip()
        if country_name:
            data["country_id"] = await self._get_or_create_by_name(Country, country_name)

        material_name = (data.pop("material_name", None) or "").strip()
        if material_name:
            data["material_id"] = await self._get_or_create_by_name(Material, material_name)

        color_name = (data.pop("color_name", None) or "").strip()
        if color_name:
            data["color_id"] = await self._get_or_create_by_name(Color, color_name)
        
        category_name = (data.pop("category_name", None) or "").strip()
        if category_name:
            data["category_id"] = await self._get_or_create_by_name(Category, category_name)

    async def on_model_delete(self, model, request):
        print(f"Удаление товара: {model.name} (ID: {model.id})")
        
        async with self.session_maker() as session:
            stmt = select(OrderItem).where(OrderItem.product_id == model.id)
            result = await session.execute(stmt)
            if result.scalars().first():
                raise Exception("Товар используется в заказах")


# Настройка для контента сайта
class SiteContentAdmin(ModelView, model=SiteContent):
    name = "Контент сайта"
    name_plural = "Контент сайта"
    column_list = [SiteContent.key, SiteContent.value, SiteContent.description]
    column_labels = {
        SiteContent.key: "Ключ",
        SiteContent.value: "Значение",
        SiteContent.description: "Описание"
    }

# Настройка для простых моделей
class CountryAdmin(ModelView, model=Country):
    name = "Страна"
    name_plural = "Страны"
    column_list = [Country.id, Country.name]
    column_labels = {
        Country.id: "ID",
        Country.name: "Название"
    }

class ColorAdmin(ModelView, model=Color):
    name = "Цвет"
    name_plural = "Цвета"
    column_list = [Color.id, Color.name, Color.code]
    column_labels = {
        Color.id: "ID",
        Color.name: "Название",
        Color.code: "Код"
    }

class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    column_list = [Category.id, Category.name, Category.slug, "parent.name"]
    form_columns = [Category.parent, Category.name, Category.slug]
    column_labels = {
        Category.id: "ID",
        Category.name: "Название",
        Category.slug: "Slug",
        Category.parent: "Родитель",
        "parent.name": "Родительская категория"
    }

class MaterialAdmin(ModelView, model=Material):
    name = "Материал"
    name_plural = "Материалы"
    column_list = [Material.id, Material.name]
    column_labels = {
        Material.id: "ID",
        Material.name: "Название"
    }

class ProductImageAdmin(ModelView, model=ProductImage):
    name = "Изображение товара"
    name_plural = "Изображения товаров"
    column_list = [ProductImage.id, ProductImage.product_id, ProductImage.url]
    column_labels = {
        ProductImage.id: "ID",
        ProductImage.product_id: "Товар",
        ProductImage.url: "URL изображения"
    }

class OrderAdmin(ModelView, model=Order):
    name = "Заказ"
    name_plural = "Заказы"
    column_list = [Order.id, Order.customer_name, Order.customer_phone, Order.total_amount, Order.status]
    column_searchable_list = [Order.customer_name, Order.customer_phone]
    column_sortable_list = [Order.total_amount, Order.status]
    column_labels = {
        Order.id: "ID",
        Order.customer_name: "Имя клиента",
        Order.customer_phone: "Телефон клиента",
        Order.total_amount: "Сумма заказа",
        Order.status: "Статус"
    }

class OrderItemAdmin(ModelView, model=OrderItem):
    name = "Позиция заказа"
    name_plural = "Позиции заказа"
    column_list = [OrderItem.order_id, OrderItem.product_id, OrderItem.quantity, OrderItem.price_at_purchase]
    column_labels = {
        OrderItem.order_id: "Заказ",
        OrderItem.product_id: "Товар",
        OrderItem.quantity: "Количество",
        OrderItem.price_at_purchase: "Цена при покупке"
    }

class ProductAttributeAdmin(ModelView, model=ProductAttribute):
    name = "Атрибут товара"
    name_plural = "Атрибуты товаров"
    column_list = [ProductAttribute.product_id, ProductAttribute.attribute_id, ProductAttribute.value_text]
    column_labels = {
        ProductAttribute.product_id: "Товар",
        ProductAttribute.attribute_id: "Атрибут",
        ProductAttribute.value_text: "Значение"
    }

class AttributeAdmin(ModelView, model=Attribute):
    name = "Атрибут"
    name_plural = "Атрибуты"
    column_list = [Attribute.id, Attribute.name]
    column_labels = {
        Attribute.id: "ID",
        Attribute.name: "Название"
    }

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