from unicodedata import category
from django.shortcuts import render
from courses.models import Course,Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from courses.models import Course, Chapter
from django.db.models import Sum


def get_courses(request):
    queryset = Course.objects.all()
    categories = Category.objects.all()
    
    context = {
        'title': 'This is test',
        'categories': categories,
        'courses': queryset,
    }
    return render(request, 'course-list.html', context=context)

class SearchView(ListView):
    model = Course
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        qs = None
        if request.GET:
            if request.GET.get("search_name"):
                qs = Course.objects.filter(Q(title__icontains=request.GET.get("search_name")) | 
                 Q(author__icontains=request.GET.get("search_name")))
        context = {
            'title': 'Courses search list',
            'search': qs,
            'word': request.GET.get("search_name"),
            'quantity': len(qs)
        }
        return render(request, 'search.html', context=context)