from django.shortcuts import render
from courses.models import Course, Chapter
from django.db.models import Sum

def get_courses(request):
    queryset = Course.objects.all()
    context = {
        'title': 'This is test',
        'courses': queryset,
    }
    return render(request, 'course-list.html', context=context)