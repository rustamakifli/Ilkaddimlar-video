from django.db import models


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=90, db_index=True)
    slug = models.SlugField(max_length=70,  db_index=True) 
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title 


class Gallery(AbstractModel):
    title = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category,related_name='galleries',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery', blank=True, null=True,)
    note = models.TextField(blank=True, null=True,)
    is_active = models.BooleanField(default=False, verbose_name="Is active?")

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title 
