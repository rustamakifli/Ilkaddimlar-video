from enum import unique
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import time
from embed_video.fields  import  EmbedVideoField
from django.urls import reverse_lazy
from datetime import datetime


User = get_user_model()


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    parent_cat = models.ForeignKey('self', related_name='sub_categories', on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(max_length=90, db_index=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title        


class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Discount(AbstractModel):
    title=models.CharField('Title', max_length=80)
    percentage=models.CharField('Percentage', max_length=20, null=True, blank=True)
    value=models.IntegerField('Value', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    parent_cat = models.ForeignKey('self', related_name='sub_specialities', on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(max_length=90, db_index=True)
    slug = models.SlugField(max_length=70, editable=False, db_index=True) 
    
    class Meta:
        verbose_name = 'Ixtisas'
        verbose_name_plural = 'Specialities'
    def __str__(self):
        return self.title  


class Author(models.Model):
    name = models.CharField(verbose_name = "First name and Last Name",max_length=90, db_index=True)
    speciality = models.ForeignKey(Speciality,related_name='speciality_authors',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='author_images', blank=True, null=True,)
    about = models.TextField(blank=True, null=True,)
    is_verified = models.BooleanField(default=False,verbose_name="Müəllimə təsdiqlənmiş badge verirsinizmi?")
    linkedin = models.URLField(max_length = 255, blank=True, null=True,)
    facebook = models.URLField(max_length = 255, blank=True, null=True,)
    twitter = models.URLField(max_length = 255, blank=True, null=True,)
    slug = models.SlugField(max_length=70, editable=False, db_index=True) 

    def __str__(self):
        return self.name 


class Course(AbstractModel):
    category = models.ForeignKey(Category,related_name='category_courses',on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, related_name='course_discount', on_delete=models.CASCADE, blank=True, null=True,)
    author = models.ForeignKey(Author,related_name='author_courses',on_delete=models.CASCADE, blank=True, null=True,)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100, db_index=True, unique=True)
    image = models.ImageField(upload_to='course_images')
    description = models.CharField(max_length=150)
    about = models.TextField()
    language = models.CharField(max_length=100)
    price = models.DecimalField(verbose_name = "Price", decimal_places = 2, max_digits=6,)
    discounted_price = models.DecimalField(verbose_name = "Final Price", decimal_places = 2, max_digits=6, null=True, blank=True,)
    teaser = EmbedVideoField()
    slug = models.SlugField(max_length=70, editable=False, db_index=True) 
    is_active = models.BooleanField(default=False,verbose_name="Is active?")
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    @property
    def course_duration(self):
        hours, minutes, seconds = 0,0,0
        for chapter in self.course_chapters.all():
            hours += chapter.chapter_duration.hour
            minutes += chapter.chapter_duration.minute
            seconds += chapter.chapter_duration.second
        if seconds > 59:
            minutes += seconds // 60
            seconds = seconds % 60
        if minutes > 59:
            hours += minutes // 60
            minutes = minutes % 60
        if hours > 23:
            return {
                'error_message':'Unknown number for durations...'
            }
        result = time(hour = hours, minute = minutes, second = seconds)
        return result 

    def get_absolute_url(self):
        return reverse_lazy('single_courses', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
            

class Chapter(AbstractModel):
    course = models.ForeignKey(Course,related_name='course_chapters',on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)

    @property
    def lesson_count(self):
        count = 0
        for lesson in self.chapter_lessons.all():
            count += 1
        return count


    @property
    def chapter_duration(self):
        hours, minutes, seconds = 0,0,0
        for lesson in self.chapter_lessons.all():
            hours += lesson.hour
            minutes += lesson.minute
            seconds += lesson.second
        if seconds > 59:
            minutes += seconds // 60
            seconds = seconds % 60
        if minutes > 59:
            hours += minutes // 60
            minutes = minutes % 60
        if hours > 23:
            return {
                'error_message':'Unknown number for durations...'
            }
        result = time(hour = hours, minute = minutes, second = seconds)
        return result   

    def __str__(self):
        return self.title


class Lesson(AbstractModel):
    chapter = models.ForeignKey(Chapter,related_name='chapter_lessons',on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    video = models.URLField(max_length = 255)
    hour = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
    minute = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    second = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])

    @property
    def lesson_duration(self):
        result = time(hour = self.hour, minute = self.minute, second = self.second)
        return result  

    def __str__(self):
        return self.title


class Comment(AbstractModel):
    CHOICES = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )

    user = models.ForeignKey(User, related_name='user_course_comments', on_delete=models.CASCADE, editable=False, null=True, default="1")
    course = models.ForeignKey(Course, related_name='course_comments', on_delete=models.CASCADE, editable=False, null=True, default="1")
    comment = models.TextField()
    in_landing = models.BooleanField('in Home Page', default=False,)
    rating = models.IntegerField(choices=CHOICES, default=5, null=True, blank=True,)
    confirm = models.BooleanField('Confirm', default=False, help_text="Confirm comment") 

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_absolute_url(self):
        return self.course.get_absolute_url()

    def __str__(self):
        return self.comment
