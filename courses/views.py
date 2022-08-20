from django.shortcuts import render
from courses.models import Course,Category

# Create your views here.
def get_courses(request):
    queryset = Course.objects.all()
    categories = Category.objects.all()
    context = {
        'title': 'This is test',
        'categories': categories,
        'courses': queryset,
    }
    return render(request, 'course-list.html', context=context)

# def courses(request):
#     queryset = Course.objects.all()
#     categories = Category.objects.all()
#     context = {
#         'title': 'This is test',
#         'categories': categories,
#         'courses': queryset,
#     }
#     return render(request, 'single-course.html', context=context)