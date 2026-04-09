from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=250, unique=True, blank=True, null=True, verbose_name="URL"
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    image = models.ImageField(
        upload_to="category_images/", blank=True, null=True, verbose_name="Изображение"
    )

    class Meta:
        db_table = "categories"
        managed = True
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        to="catalog.Category", on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество")
    image = models.ImageField(
        upload_to="product_images/", blank=True, null=True, verbose_name="Изображение"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "products"
        managed = True
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} | {self.price} | {self.stock}"
