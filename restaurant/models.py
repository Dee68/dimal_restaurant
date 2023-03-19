from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.


class Table(models.Model):
    TABLE_TYPE = (
        ('basic', 'Basic'),
        ('vip', 'Vip'),
    )
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    number = models.IntegerField()
    gender = models.CharField(choices=TABLE_TYPE, default='basic', max_length=5)
    capacity = models.IntegerField(default=1)
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, upload_to="tables/")
    description = models.TextField(default='Book a table and  have taste of this exotic meal.')

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    # def get_absolute_url(self, *args, **kwargs):
    #     return reverse('restaurant:table-detail', args=[self.id, self.slug])

    def __str__(self):
        return f'Table number {self.number} with a capacity of {self.capacity}'


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    reserve_start = models.DateTimeField()
    reserve_end = models.DateTimeField()
    reserved_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def get_reserve_start(self):
        return self.reserve_start.strftime('%m/%d/%Y %I:%M %p')

    @property
    def get_reserve_end(self):
        return self.reserve_end.strftime('%m/%d/%Y %I:%M %p')

    def __str__(self):
        return f'{self.customer.username} reserved {self.table.title}'


class Review(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table_review')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} reviewed {self.table.title}'
