from django.db import models
from datetime import date

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Racer(models.Model):
    """Гонщики + Производители"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="racers/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('racer_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Гонщики и Производители"
        verbose_name_plural = "Гонщики и Производители"


class Season(models.Model):
    """Сезон"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"


class Model(models.Model):
    """Модель"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="models/")
    year = models.PositiveSmallIntegerField("Дата сборки", default=2004)
    country = models.CharField("Страна", max_length=30)
    manufacturers = models.ManyToManyField(Racer, verbose_name="Производитель", related_name="moto_manufacturer")
    racers = models.ManyToManyField(Racer, verbose_name="Гонщики", related_name="moto_racer")
    season = models.ManyToManyField(Season, verbose_name="Сезон")
    world = models.DateField("Выход на рынок", default=date.today)
    price = models.PositiveIntegerField("Цена за рубежом", default=0, help_text="Указать сумму в долларах")
    price_in_rus = models.PositiveIntegerField("Цена в России", default=0, help_text="Указать сумму в долларах")
    price_market = models.PositiveIntegerField("Цена перекупом", default=0, help_text="Указать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('model_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class Image(models.Model):
    """Фото"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="moto_images/")
    model = models.ForeignKey(Model, verbose_name="Модель", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото модели"
        verbose_name_plural = "Фото модели"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name="Модель")

    def __str__(self):
        return f"{self.star} - {self.model}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    model = models.ForeignKey(Model, verbose_name="Модель", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.model}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
