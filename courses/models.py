from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import time

User = get_user_model()


class AbsrtactModel(models.Model):
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


class Discount(AbsrtactModel):
    title=models.CharField('Title', max_length=80)
    percentage=models.CharField('Percentage', max_length=20, null=True, blank=True)
    value=models.IntegerField('Value', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Course(AbsrtactModel):
    category = models.ForeignKey(Category,related_name='category_courses',on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', related_name='course_discount', on_delete=models.CASCADE, blank=True, null=True,)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='course_images')
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    about = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    price = models.DecimalField(verbose_name = "Price", decimal_places = 2, max_digits=6,)
    discounted_price = models.DecimalField(verbose_name = "Discounted Price", decimal_places = 2, max_digits=6, null=True, blank=True, help_text="""
        Buraya hər hansı məbləğ qeyd etməyə ehtiyac yoxdur. Daxil etdiyiniz qiymət və endirim (əgər varsa) nəzərə alınaraq avtomatik hesablanma aparılır.""")
    teaser = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    # duration field for MVC, no need for API
    duration = models.CharField(max_length=100) 

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

    def __str__(self):
        return self.title
            

class Chapter(AbsrtactModel):
    course = models.ForeignKey(Course,related_name='course_chapters',on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    # duration field for MVC, no need for API
    duration = models.CharField(max_length=100)

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


class Lesson(AbsrtactModel):
    chapter = models.ForeignKey(Chapter,related_name='chapter_lessons',on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    video = models.CharField(max_length=255)
    hour = models.PositiveIntegerField(default=00, validators=[MinValueValidator(0), MaxValueValidator(50)])
    minute = models.PositiveIntegerField(default=00, validators=[MinValueValidator(0), MaxValueValidator(59)])
    second = models.PositiveIntegerField(default=00, validators=[MinValueValidator(0), MaxValueValidator(59)])
    # duration field for MVC, no need for API
    duration = models.CharField(max_length=100)

    @property
    def lesson_duration(self):
        result = time(hour = self.hour, minute = self.minute, second = self.second)
        return result  

    def __str__(self):
        return self.title


class Comment(AbsrtactModel):
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
    rating = models.IntegerField(choices=CHOICES, default=5, null=True, blank=True,)
    confirm = models.BooleanField('Confirm', default=False, help_text="Confirm comment") 

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        if self.confirm:
            return f"{self.comment} - Comment is confirmed"
        return self.comment


        