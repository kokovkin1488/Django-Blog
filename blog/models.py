from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):

    # db_index - индексация по этому полю
    title = models.CharField(max_length=150, db_index=True)

    # буквы, цифры, _, -
    # включили уникальность
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    # blank - может быть пустым
    body = models.TextField(blank=True, db_index=True)

    # auto_now_add=True - будет выполняться при сохранении в БД
    date_pub = models.DateTimeField(auto_now_add=True)

    # related_name = свойство, которое появится у тегов
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    # генерируем слаг при сохранении
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        # вызываыем метод у супер класса
        super().save(*args, **kwargs)

    # возвращает абсолютную ссылку на пост
    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    # сортировать посты по дате публикации в обратном порядке
    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-title']