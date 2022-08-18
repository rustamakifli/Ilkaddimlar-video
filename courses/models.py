from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AbsrtactModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
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
    title = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    about = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    ex_price = models.DecimalField(verbose_name = "Price", decimal_places = 2, max_digits=6,)
    discount = models.ForeignKey('Discount', related_name='course_discount', on_delete=models.CASCADE, blank=True, null=True,)
    price = models.DecimalField(verbose_name = "Discounted Price", decimal_places = 2, max_digits=6, null=True, blank=True, help_text="""
        Buraya hər hansı məbləğ qeyd etməyə ehtiyac yoxdur. Daxil etdiyiniz qiymət və endirim (əgər varsa) nəzərə alınaraq avtomatik hesablanma aparılır.""")
    teaser = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Chapter(AbsrtactModel):
    title = models.CharField(max_length=255, db_index=True)
    course = models.ForeignKey(Course,related_name='chapters_courses',on_delete=models.CASCADE)
    duration = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Videos(AbsrtactModel):
    title = models.CharField(max_length=255, db_index=True)
    chapter = models.ForeignKey(Chapter,related_name='videos_chapters',on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)

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
    user = models.ForeignKey(User, related_name='user_course_commennts', on_delete=models.CASCADE, editable=False, null=True, default="1")
    course = models.ForeignKey(User, related_name='course_commennts', on_delete=models.CASCADE, editable=False, null=True, default="1")
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