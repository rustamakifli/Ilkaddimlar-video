from django.shortcuts import render
from courses.models import Course

# Create your views here.
def get_courses(request):
    queryset = Course.objects.all()
    context = {
        'title': 'This is test',
        'courses': queryset,
    }
    return render(request, 'course-list.html', context=context)