from django.shortcuts import render
from courses.models import Course, Category, Discount, Tag, Comment, StudentCourse, Author
from order.models import Cart_Item
from courses.forms import CourseCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from courses.models import Course, Chapter,StudentCourse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.db.models import Count


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
        author_id = self.request.GET.get('author_id') 
        discount = self.request.GET.get('discount') 
        min_price = self.request.GET.get('min_price', 0) 
        max_price = self.request.GET.get('max_price', 9999)

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        if discount:
            queryset = queryset.filter(discount__isnull=False)
        if max_price and min_price:
            queryset = queryset.filter(discounted_price__range=(min_price, max_price))
        elif min_price:
            queryset = queryset.filter(discounted_price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(discounted_price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_courses'] = Course.objects.filter(is_active=True)
        context['discounted_courses'] = Course.objects.filter(discount__isnull=False)
        context['categories'] = Category.objects.annotate(number_of_courses = Count("category_courses")).all()
        context['popularcourses'] = Course.objects.all()[0:3]
        context['tags'] = Tag.objects.all()
        context['authors'] = Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6]


        return context


class CourseDetailView(DetailView,CreateView):
    model = Course
    template_name = 'single-course.html'
    context_object_name = 'course'
    form_class = CourseCommentForm

    def form_valid(self, form):
        form.instance.course_id = self.request.POST.get("course_id", None)
        form.instance.user = self.request.user
        form.instance.rating = self.request.POST.get("star_value", None)
        return super().form_valid(form)

    def get_object(self):
        return Course.objects.filter(slug=self.kwargs['slug']).first()

    def get_success_url(self):
        return reverse_lazy('single_courses', kwargs = {'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_courses'] = Course.objects.filter(is_active=True)
        context['discounted_courses'] = Course.objects.filter(discount__isnull=False)
        context['categories'] = Category.objects.annotate(number_of_courses = Count("category_courses")).all()
        context['popularcourses'] = Course.objects.all()[0:3]
        context['tags'] = Tag.objects.all()
        context['authors'] = Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6]

        context['related_courses'] = Course.objects.filter(category=Course.objects.get(slug=self.kwargs.get('slug')).category, is_active=True).exclude(slug=self.kwargs.get('slug'))[0:3]
        context['comment_form'] = CourseCommentForm(
            data=self.request.POST)
        context['comments'] = Comment.objects.filter(confirm=True,
            course__slug=self.kwargs.get('slug')).all()
        context['categories'] = Category.objects.all()
        context['course_tags'] = Tag.objects.filter(
            course__slug=self.kwargs.get('slug'))
        context['course_chapters'] = Chapter.objects.filter(
            course__slug=self.kwargs.get('slug'))
        # odenis edilmis kurslar
        paid_courses = Cart_Item.objects.filter(is_paid = True)
        # request gonderen userin odenis etdiyi kurslar
        user_paid_courses = paid_courses.filter(cart__user=self.request.user.id)
        # userin baxmaq istediyi kurs
        user_wants_to_see_this_course = Course.objects.filter(slug=self.kwargs.get('slug')).first()
        # userin baxmaq istediyi kurs onun odenis etdiyi kurslarin icerisinde var mi?
        permit = user_paid_courses.filter(course=user_wants_to_see_this_course.id).exists()    
        
        context['permit'] = permit

        return context


class AuthorDetailView (DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs = {'pk':self.kwargs['pk']})


class SearchView(ListView):
    model = Course
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        qs = None
        if request.GET:
            if request.GET.get("search_name"):
                qs = Course.objects.filter(Q(title__icontains=request.GET.get("search_name")) | 
                 Q(author__name__icontains=request.GET.get("search_name")))
                print('````````````````````````````````````')
                print('search works')
        context = {
            'title': 'Courses search list',
            'search': qs,
            'word': request.GET.get("search_name"),
        }
        if qs:
            quantity = {'quantity':len(qs)}
            context.update(quantity)
        return render(request, 'search.html', context=context)


class UpdateCommentView(LoginRequiredMixin, UpdateView):
    form_class = CourseCommentForm
    model = Comment
    template_name = 'edit_comment.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(UpdateCommentView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        star = self.request.POST.get("star_value",None)
        form.instance.rating = star
        form.instance.confirm = False
        return super().form_valid(form)


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "confirm_delete_comment.html"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteCommentView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    # def form_valid(self, form):
    #     print()
    #     self.object.delete()
    #     return super().form_valid(form)

    def get_success_url(self): 
        return reverse_lazy( 'single_courses', kwargs = {'slug':self.request.POST.get("course_slug", None) })

class UserCoursesListView(LoginRequiredMixin, ListView):
    template_name = 'user-course-list.html'
    model = StudentCourse
    context_object_name = 'courses'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        userinkurslari = StudentCourse.objects.filter(user=self.request.user.id)
        paid_courses = userinkurslari.filter(is_paid = True)
        pending_courses = userinkurslari.filter(is_paid = False)
        context['paid_courses'] = paid_courses
        context['pending_courses'] = pending_courses

        return context

class SingleblogView(TemplateView):
    template_name = 'blog-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogView(TemplateView):
    template_name = 'blog-archive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context