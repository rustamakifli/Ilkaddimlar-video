from django.db import models

# Create your models here.


class AbsrtactModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Cart(AbsrtactModel):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, default="1")
    course = models.ManyToManyField(
        "courses.Course", blank=True)
    is_ordered = models.BooleanField(verbose_name="Is Ordered?", default=False)
    ordered_at = models.DateTimeField(
        verbose_name="Ordered at", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"


class Cart_Item(AbsrtactModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="User_Cart")
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, blank=True, null=True, related_name="Product_Cart")
    price = models.FloatField(verbose_name="Price", default=0.00)


    def __str__(self) -> str:
        return f"{self.cart}"