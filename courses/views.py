
from django.shortcuts import render
from courses.models import Course,Category
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.core.paginator import Paginator
from courses.models import Course, Chapter


def PaginatorCourseList(request):
    course_list = Course.objects.filter(
        is_active=True).order_by('created_at')
    course_len = Course.objects.filter(is_active=True).count()

    paginator = Paginator(course_list, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET:
        course_list = Course.objects.order_by('created_at')
        # if request.GET.get("category_name"):
        #     course_list = course_list.filter(
        #         category__parent__title=request.GET.get("category_name"))
 

        paginator = Paginator(course_list, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'Course-list ',
        'categories': Category.objects.all(),
        'course_len': course_len,

    }
    return render(request, 'course-list.html', context=context)

class CourseView(DetailView):
    model = Course
    context_object_name = 'courses'
    template_name = 'single-course.html'

    def get_object(self):
        return Course.objects.filter(id=self.kwargs['pk']).first()

    def get_success_url(self):
        courseid = self.kwargs['pk']
        return reverse_lazy('single_courses', kwargs = {'pk':courseid})

    # # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     single_product = self.get_object()
    #     parent_product = single_product.product

    #     context = 

    #     # context['product_version_tags'] = Tag.objects.filter(
    #     #     product__id=parent_product.id
    #     # )
    #     return context

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