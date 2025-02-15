from django.db import models

# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Coupon(AbstractModel):
    code = models.CharField(max_length=255, unique=True)
    discount = models.FloatField(default=0.00)
    is_available = models.PositiveIntegerField(default=1)
    used = models.IntegerField(default=0,editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}"

class Cart(AbstractModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="userin_kartlari")
    course = models.ManyToManyField("courses.Course", blank=True,related_name = "course_cart")
    is_ordered = models.BooleanField(verbose_name="Is Ordered?", default=False)
    ordered_at = models.DateTimeField(
        verbose_name="Ordered at", null=True, blank=True)
    coupon = models.ForeignKey(
        Coupon, null=True, blank=True, verbose_name="Coupon", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}"


class Cart_Item(AbstractModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="user_cart")
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, blank=True, null=True, related_name="Product_Cart")
    price = models.FloatField(verbose_name="Price", default=0.00)
    is_paid = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.cart}"

class Wishlist(AbstractModel):
    user = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, default="")
    course = models.ManyToManyField(
        'courses.Course', blank=True, related_name='course_wishlist')

    def __str__(self):
        return f"{self.user}"

