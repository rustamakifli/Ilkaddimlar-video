
from django.shortcuts import render
from courses.models import Course, Category, Tag, Comment
from courses.models import Course,Category
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.base import View
from courses.models import Course, Chapter,StudentCourse,Lesson
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CourseListView(ListView):
    template_name = 'course-list.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        category_id = self.request.GET.get('category_id') 
        tag_id = self.request.GET.get('tag_id') 
        discount = self.request.GET.get('discount') 
        min_price = self.request.GET.get('min_price', 0) 
        max_price = self.request.GET.get('max_price', 9999)

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        if discount:
            queryset = queryset.filter(discount=True)
        if max_price and min_price:
            queryset = queryset.filter(discounted_price__range=(min_price, max_price))
        elif min_price:
            queryset = queryset.filter(discounted_price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(discounted_price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        return context


# class CourseDetailView(DetailView,CreateView):
class CourseDetailView(DetailView):
    model = Course
    template_name = 'single-course.html'
    context_object_name = 'course'
    # form_class = CourseCommentForm

    # def form_valid(self, form):
    #     form.instance.course_id = self.kwargs['pk']
    #     form.instance.user = self.request.user
    #     star = self.request.POST.get("star_value",None)
    #     form.instance.rating = star
    #     return super().form_valid(form)

    def get_object(self):
        return Course.objects.filter(id=self.kwargs['pk']).first()

    def get_success_url(self):
        return reverse_lazy('single_courses', kwargs = {'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_course = self.get_object()

        context['related_courses'] = Course.objects.filter(category=Course.objects.get(pk=self.kwargs.get('pk')).category, is_active=True).exclude(pk=self.kwargs.get('pk'))[0:3]

        # context['comment_form'] = CourseCommentForm(
        #     data=self.request.POST)

        # context['comments'] = Comment.objects.filter(confirm=True,
        #     course_id=self.kwargs.get('pk')).all()
        context['categories'] = Category.objects.all()
        context['course_tags'] = Tag.objects.filter(
            course__id=self.kwargs.get('pk'))
        context['course_chapters'] = Chapter.objects.filter(
            course__id=self.kwargs.get('pk'))
        return context

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'single-lesson.html'
    context_object_name = 'lesson'

    def get_object(self):
        return Lesson.objects.filter(id=self.kwargs['pk']).first()

    def get_success_url(self):
        return reverse_lazy('single_lesson', kwargs = {'pk':self.kwargs['pk']})

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

# class MyCourseView(LoginRequiredMixin, View):
#     def get(self, request):
#         courses = StudentCourse.objects.filter(user=request.user)
#         current = "my_course"
#         return render(request, "mycourse.html", {
#             'courses': courses,
#             'current': current
#         })