from django.urls import path
from gallery.views import GalleryListView

urlpatterns = [
    path('gallery/', GalleryListView.as_view(), name="gallery"),

]