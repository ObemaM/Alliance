from pathlib import Path
import re
import shutil
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqladmin import Admin, ModelView
from wtforms import FileField, MultipleFileField, SelectField, StringField
from wtforms.validators import Optional

from config import settings
from database import engine
from main import app
from models import (
    Attribute,
    Category,
    Color,
    Country,
    Material,
    Order,
    OrderItem,
    Product,
    ProductAttribute,
    ProductImage,
    SiteContent,
)


admin = Admin(
    app,
    engine,
    templates_dir=str(Path(__file__).resolve().parent / "templates"),
    title="Панель администратора",
)


def sanitize_filename(name: str) -> str:
    if not name:
        return "file"
    name = name.replace("\\", "/").split("/")[-1]
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def normalize_uploads(value) -> list:
    if not value:
        return []

    uploads = value if isinstance(value, (list, tuple)) else [value]
    return [upload for upload in uploads if getattr(upload, "filename", "").strip()]


def validate_upload(upload, allowed_extensions: list[str] | tuple[str, ...]) -> str:
    filename = sanitize_filename(getattr(upload, "filename", ""))
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed_extensions:
        raise ValueError(f"Разрешены только {'/'.join(allowed_extensions)}")
    return ext


def save_upload_image(upload, *, prefix: str, allowed_extensions: list[str] | tuple[str, ...]) -> str:
    ext = validate_upload(upload, allowed_extensions)
    new_name = f"{prefix}-{uuid.uuid4().hex[:6]}.{ext}"
    upload_dir = Path("uploads/images")
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / new_name

    upload.file.seek(0)
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    return f"/uploads/images/{new_name}"


def delete_upload_image(image_url: str | None) -> None:
    if not image_url:
        return

    normalized = image_url.replace("\\", "/").strip()
    if not normalized.startswith("/uploads/images/"):
        return

    file_path = Path(__file__).resolve().parent / normalized.lstrip("/")
    if file_path.exists() and file_path.is_file():
        file_path.unlink()


def slugify_category_name(name: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", name.lower(), flags=re.UNICODE)
    slug = re.sub(r"[-\s]+", "-", slug, flags=re.UNICODE).strip("-_")
    return slug or f"category-{uuid.uuid4().hex[:6]}"


class ThemedModelView(ModelView):
    details_template = "sqladmin/custom_details.html"


class ProductAdmin(ThemedModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"
    icon = "ti ti-package"
    attribute_slots = 8

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
    ]
    column_details_list = [
        Product.id,
        Product.name,
        Product.description,
        Product.category,
        Product.color,
        Product.material,
        Product.country,
        Product.price,
        Product.quantity,
        Product.pack_quantity,
        Product.weight,
        Product.created_at,
        Product.updated_at,
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

    async def scaffold_form(self, rules=None):
        form = await super().scaffold_form(rules)

        async with self.session_maker(expire_on_commit=False) as session:
            result = await session.execute(select(Attribute).order_by(Attribute.name))
            attributes = result.scalars().all()

        attribute_choices = [
            (0, ""),
            (-1, "Ввести новую характеристику"),
        ] + [
            (attribute.id, attribute.name) for attribute in attributes
        ]

        class ProductForm(form):
            category_name = StringField("Категория", validators=[Optional()], render_kw={"class": "form-control"})
            color_name = StringField("Цвет", validators=[Optional()], render_kw={"class": "form-control"})
            material_name = StringField("Материал", validators=[Optional()], render_kw={"class": "form-control"})
            country_name = StringField("Страна", validators=[Optional()], render_kw={"class": "form-control"})
            file_upload = MultipleFileField(
                "Изображения товара",
                validators=[Optional()],
                render_kw={"class": "form-control", "multiple": True, "accept": "image/*"},
            )

            def __init__(self, *args, **kwargs):
                formdata = args[0] if args else kwargs.get("formdata")
                obj = kwargs.get("obj")
                super().__init__(*args, **kwargs)

                if formdata is None and obj is not None:
                    attributes_data = list(getattr(obj, "product_attributes", []) or [])
                    for idx, product_attribute in enumerate(attributes_data[: ProductAdmin.attribute_slots], start=1):
                        getattr(self, f"attribute_id_{idx}").data = getattr(product_attribute, "attribute_id", 0) or 0
                        getattr(self, f"attribute_value_{idx}").data = product_attribute.value_text or ""

        for idx in range(1, self.attribute_slots + 1):
            setattr(
                ProductForm,
                f"attribute_id_{idx}",
                SelectField(
                    "Характеристика",
                    choices=attribute_choices,
                    coerce=int,
                    validators=[Optional()],
                    render_kw={"class": "form-select"},
                ),
            )
            setattr(
                ProductForm,
                f"attribute_name_{idx}",
                StringField(
                    "Новая характеристика",
                    validators=[Optional()],
                    render_kw={"class": "form-control"},
                ),
            )
            setattr(
                ProductForm,
                f"attribute_value_{idx}",
                StringField(
                    "Значение",
                    validators=[Optional()],
                    render_kw={"class": "form-control"},
                ),
            )

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

    async def _get_or_create_category_by_name(self, name: str) -> int:
        normalized = name.strip()
        async with self.session_maker(expire_on_commit=False) as session:
            stmt = select(Category).where(func.lower(Category.name) == normalized.lower())
            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj is not None:
                return obj.id

            base_slug = slugify_category_name(normalized)
            slug = base_slug
            index = 2

            while True:
                slug_stmt = select(Category).where(func.lower(Category.slug) == slug.lower())
                slug_result = await session.execute(slug_stmt)
                if slug_result.scalars().first() is None:
                    break
                slug = f"{base_slug}-{index}"
                index += 1

            obj = Category(name=normalized, slug=slug)
            session.add(obj)
            await session.flush()
            await session.commit()
            return obj.id

    async def _get_or_create_attribute_by_name(self, name: str) -> int:
        return await self._get_or_create_by_name(Attribute, name)

    async def _parse_attribute_slots(self, data: dict) -> list[tuple[int, str]]:
        parsed_attributes: dict[int, str] = {}

        for idx in range(1, self.attribute_slots + 1):
            selected_id = data.pop(f"attribute_id_{idx}", 0) or 0
            new_name = (data.pop(f"attribute_name_{idx}", None) or "").strip()
            value_text = (data.pop(f"attribute_value_{idx}", None) or "").strip()

            if not selected_id and not new_name and not value_text:
                continue

            if not value_text:
                raise ValueError("Для характеристики нужно указать значение")

            if int(selected_id) == -1:
                if not new_name:
                    raise ValueError("Введите название новой характеристики")
                attribute_id = await self._get_or_create_attribute_by_name(new_name)
            elif int(selected_id) > 0:
                attribute_id = int(selected_id)
            else:
                raise ValueError("Выберите характеристику или введите новую")

            parsed_attributes[attribute_id] = value_text

        return list(parsed_attributes.items())

    def form_edit_query(self, request):
        stmt = super().form_edit_query(request)
        return stmt.options(
            selectinload(Product.product_attributes).selectinload(ProductAttribute.attribute)
        )

    def details_query(self, request):
        stmt = super().details_query(request)
        return stmt.options(
            selectinload(Product.category),
            selectinload(Product.color),
            selectinload(Product.material),
            selectinload(Product.country),
            selectinload(Product.product_images),
            selectinload(Product.product_attributes).selectinload(ProductAttribute.attribute),
        )

    async def on_model_change(self, data: dict, model, is_created: bool, request):
        uploads = normalize_uploads(data.pop("file_upload", None))
        for upload in uploads:
            validate_upload(upload, settings.ALLOWED_EXTENSIONS)
        model._pending_product_uploads = uploads
        model._pending_product_attributes = await self._parse_attribute_slots(data)

        country_name = (data.pop("country_name", None) or "").strip()
        if country_name:
            data["country"] = await self._get_or_create_by_name(Country, country_name)

        material_name = (data.pop("material_name", None) or "").strip()
        if material_name:
            data["material"] = await self._get_or_create_by_name(Material, material_name)

        color_name = (data.pop("color_name", None) or "").strip()
        if color_name:
            data["color"] = await self._get_or_create_by_name(Color, color_name)

        category_name = (data.pop("category_name", None) or "").strip()
        if category_name:
            data["category"] = await self._get_or_create_category_by_name(category_name)

    async def after_model_change(self, data: dict, model, is_created: bool, request):
        uploads = normalize_uploads(getattr(model, "_pending_product_uploads", []))
        attributes = getattr(model, "_pending_product_attributes", None)

        async with self.session_maker(expire_on_commit=False) as session:
            if attributes is not None:
                existing_result = await session.execute(
                    select(ProductAttribute).where(ProductAttribute.product_id == model.id)
                )
                for product_attribute in existing_result.scalars().all():
                    await session.delete(product_attribute)

                for attribute_id, value_text in attributes:
                    session.add(
                        ProductAttribute(
                            product_id=model.id,
                            attribute_id=attribute_id,
                            value_text=value_text,
                        )
                    )

            for upload in uploads:
                image_url = save_upload_image(
                    upload,
                    prefix="product",
                    allowed_extensions=settings.ALLOWED_EXTENSIONS,
                )
                session.add(ProductImage(product_id=model.id, url=image_url))

            await session.commit()

        model._pending_product_uploads = []
        model._pending_product_attributes = []

    async def on_model_delete(self, model, request):
        print(f"Удаление товара: {model.name} (ID: {model.id})")

        async with self.session_maker(expire_on_commit=False) as session:
            stmt = select(OrderItem).where(OrderItem.product_id == model.id)
            result = await session.execute(stmt)
            if result.scalars().first():
                raise Exception("Товар используется в заказах")


            images_result = await session.execute(
                select(ProductImage).where(ProductImage.product_id == model.id)
            )
            for product_image in images_result.scalars().all():
                delete_upload_image(product_image.url)
                await session.delete(product_image)

            attributes_result = await session.execute(
                select(ProductAttribute).where(ProductAttribute.product_id == model.id)
            )
            for product_attribute in attributes_result.scalars().all():
                await session.delete(product_attribute)

            await session.commit()


class SiteContentAdmin(ThemedModelView, model=SiteContent):
    name = "Контент сайта"
    name_plural = "Контент сайта"
    icon = "ti ti-file-text"

    column_list = [SiteContent.key, SiteContent.value, SiteContent.description]
    form_columns = [SiteContent.key, SiteContent.value, SiteContent.description]
    column_labels = {
        SiteContent.key: "Ключ",
        SiteContent.value: "Значение",
        SiteContent.description: "Описание",
    }

    async def scaffold_form(self, rules=None):
        form = await super().scaffold_form(rules)
        form.file_upload = FileField("Загрузить файл")
        return form

    async def on_model_change(self, data, model, is_created, request):
        upload = data.pop("file_upload", None)
        if upload and hasattr(upload, "filename") and upload.filename:
            new_value = save_upload_image(
                upload,
                prefix="logo",
                allowed_extensions=["jpg", "jpeg", "png"],
            )
            data["value"] = new_value
            model.value = new_value

        await super().on_model_change(data, model, is_created, request)


class CountryAdmin(ThemedModelView, model=Country):
    name = "Страна"
    name_plural = "Страны"
    icon = "ti ti-world"

    column_list = [Country.id, Country.name]
    column_labels = {
        Country.id: "ID",
        Country.name: "Название",
    }


class ColorAdmin(ThemedModelView, model=Color):
    name = "Цвет"
    name_plural = "Цвета"
    icon = "ti ti-palette"

    column_list = [Color.id, Color.name, Color.code]
    column_labels = {
        Color.id: "ID",
        Color.name: "Название",
        Color.code: "Код",
    }


class CategoryAdmin(ThemedModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    icon = "ti ti-category"

    column_list = [Category.id, Category.name, Category.slug, "parent.name"]
    form_columns = [Category.parent, Category.name, Category.slug]
    column_labels = {
        Category.id: "ID",
        Category.name: "Название",
        Category.slug: "Slug",
        Category.parent: "Родитель",
        "parent.name": "Родительская категория",
    }


class MaterialAdmin(ThemedModelView, model=Material):
    name = "Материал"
    name_plural = "Материалы"
    icon = "ti ti-texture"

    column_list = [Material.id, Material.name]
    column_labels = {
        Material.id: "ID",
        Material.name: "Название",
    }


class ProductImageAdmin(ThemedModelView, model=ProductImage):
    name = "Изображение товара"
    name_plural = "Изображения товаров"
    icon = "ti ti-photo"

    column_list = [ProductImage.product, ProductImage.url]
    form_columns = [ProductImage.product]
    column_labels = {
        ProductImage.product: "Товар",
        ProductImage.url: "URL изображения",
    }

    async def scaffold_form(self, rules=None):
        form = await super().scaffold_form(rules)
        form.file_upload = FileField("Загрузить изображение", render_kw={"class": "form-control", "accept": "image/*"})
        return form

    async def on_model_change(self, data, model, is_created, request):
        upload = data.pop("file_upload", None)
        if upload and hasattr(upload, "filename") and upload.filename:
            old_url = getattr(model, "url", None) if not is_created else None
            new_url = save_upload_image(
                upload,
                prefix="product",
                allowed_extensions=settings.ALLOWED_EXTENSIONS,
            )
            if old_url and old_url != new_url:
                delete_upload_image(old_url)
            data["url"] = new_url
            model.url = new_url

        await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model, request):
        delete_upload_image(model.url)


class OrderAdmin(ThemedModelView, model=Order):
    name = "Заказ"
    name_plural = "Заказы"
    icon = "ti ti-shopping-bag"

    column_list = [Order.id, Order.customer_name, Order.customer_phone, Order.total_amount, Order.status]
    column_searchable_list = [Order.customer_name, Order.customer_phone]
    column_sortable_list = [Order.total_amount, Order.status]
    column_labels = {
        Order.id: "ID",
        Order.customer_name: "Имя клиента",
        Order.customer_phone: "Телефон клиента",
        Order.total_amount: "Сумма заказа",
        Order.status: "Статус",
    }


class OrderItemAdmin(ThemedModelView, model=OrderItem):
    name = "Позиция заказа"
    name_plural = "Позиции заказа"
    icon = "ti ti-list-details"

    column_list = [OrderItem.order_id, OrderItem.product_id, OrderItem.quantity, OrderItem.price_at_purchase]
    column_labels = {
        OrderItem.order_id: "Заказ",
        OrderItem.product_id: "Товар",
        OrderItem.quantity: "Количество",
        OrderItem.price_at_purchase: "Цена при покупке",
    }


class ProductAttributeAdmin(ThemedModelView, model=ProductAttribute):
    name = "Атрибут товара"
    name_plural = "Атрибуты товаров"
    icon = "ti ti-adjustments"

    column_list = [ProductAttribute.product_id, ProductAttribute.attribute_id, ProductAttribute.value_text]
    column_labels = {
        ProductAttribute.product_id: "Товар",
        ProductAttribute.attribute_id: "Атрибут",
        ProductAttribute.value_text: "Значение (укажите единицу измерения)",
    }


class AttributeAdmin(ThemedModelView, model=Attribute):
    name = "Атрибут"
    name_plural = "Атрибуты"
    icon = "ti ti-tag"

    column_list = [Attribute.id, Attribute.name]
    column_labels = {
        Attribute.id: "ID",
        Attribute.name: "Название",
    }


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
