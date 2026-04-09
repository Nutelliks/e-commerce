from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    slug = models.CharField(max_length=250, unique=True, verbose_name="URL")
    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    class Meta:
        db_table = 'categories'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'