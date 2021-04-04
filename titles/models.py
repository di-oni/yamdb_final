from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from .utils import current_year, max_value_current_year

User = get_user_model()


class Category(models.Model):
    """The model of titles category. Inherited from models.Model."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    slug = models.SlugField(max_length=40, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """The model of titles genre. Inherited from models.Model."""
    name = models.CharField(max_length=100, verbose_name='Имя')
    slug = models.SlugField(max_length=40, unique=True, verbose_name='Slug')
    lookup_field = 'slug'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """The model of title. Inherited from models.Model."""
    name = models.CharField(max_length=200, verbose_name='Имя')
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[
            MinValueValidator(1000),
            max_value_current_year,
        ]
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, related_name='titles')

    class Meta:
        ordering = ['-year', ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """The model of titles review. Inherited from models.Model."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Пользовательский отзыв о произведении'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='The minimum score must be 1'),
            MaxValueValidator(10, message='The maximum score must be 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True,
        null=True
    )

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        author = self.author.username
        title = self.title.name
        rating = self.score
        result = f"{author}'s review on {title} with a score of {rating}"
        return result


class Comment(models.Model):
    """The model of reviews comment. Inherited form models.Model."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Пользовательский комментарий на отзыв о произведении'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date', ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        author = self.author.username
        review_author = self.review.author.username
        date = self.pub_date
        result = (f"{author}'s comment on {review_author}"
                  f"in {date:%Y-%m-%d %H:%M}")
        return result
