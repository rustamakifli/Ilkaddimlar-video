from django.views.generic import ListView
from gallery.models import Category, Gallery
from django.db.models import Count


class GalleryListView(ListView):
    template_name = 'gallery.html'
    model = Gallery
    context_object_name = 'images'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        filter = self.request.GET.get('filter') 

        if filter:
            queryset = queryset.filter(category__slug=filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(number_of_images = Count("galleries")).all()
        return context