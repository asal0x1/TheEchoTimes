from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class CategoriesAbout(models.Model):
    title = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categories_about',
    )
    name = models.CharField(blank=True, null=True, max_length=100)
    short_description = models.TextField(blank=True)
    date = models.DateField(blank=True)

    image = models.ImageField(upload_to="News")
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        self.name = self.name
        return self.name

class News(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField()
    heading2 = models.TextField(blank=True, null=True)
    heading2_desc = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to='News')
    image1 = models.ImageField(upload_to='News', blank=True, null=True)
    image2 = models.ImageField(upload_to='News', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    author_name = models.TextField(blank=True, null=True)
    author_image = models.ImageField(upload_to='News', blank=True, null=True)
    author_desc= models.TextField(blank=True, null=True, default='')

    views = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author } on {self.news}"

