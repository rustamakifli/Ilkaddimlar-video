from multiprocessing import context
from urllib import request
from django.shortcuts import render
from courses.models import Course, Category, Tag, Comment, Author
from order.models import Cart_Item
from courses.forms import CourseCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from courses.models import Course, Chapter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count



class CourseListView(ListView):
    template_name = 'course-list.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 4

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


# class UserCourseListView(LoginRequiredMixin, DetailView):
#     model = Course
#     template_name = 'user-course-list.html'

#     def get_context_data(self, **kwargs):
#         context = super(UserCourseListView,self).get_context_data(**kwargs)
#         # print(context)
#         # odenis edilmis kurslar
#         paid_courses = Cart_Item.objects.filter(is_paid = True)
#         # print(paid_courses)
#         # request gonderen userin odenis etdiyi kurslar
#         user_paid_courses = paid_courses.filter(cart__user=self.request.user.id)
#         print(user_paid_courses)
#         context['user_paid_courses'] = user_paid_courses
#         return context

#     def dispatch(self, request,*args, **kwargs):
#         print("hey")
#         if not self.request.user.is_authenticated:
#             return render(request,"404.html")
#         return render(request, 'user-course-list.html')

class UserCourseView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'user-course-list.html'

    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated:
            return render(request,'404.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) :
        context = super(UserCourseView,self).get_context_data(**kwargs)
        # print(context)
        courses = Course.objects.all()
        paid_courses = Cart_Item.objects.filter(is_paid = True)
        # print(paid_courses)
        # request gonderen userin odenis etdiyi kurslar
        user_paid_courses = paid_courses.filter(cart__user=self.request.user.id)
        # print(user_paid_courses)
        context['user_paid_courses'] = courses
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
        course = self.get_object()
        if course.users_wishlist.filter(id=self.request.user.id).exists():
            wishlist = True
        else:
            wishlist = False
        context = super().get_context_data(**kwargs)
        context['related_courses'] = Course.objects.filter(category=Course.objects.get(slug=self.kwargs.get('slug')).category, is_active=True).exclude(slug=self.kwargs.get('slug'))
        context['comment_form'] = CourseCommentForm(
            data=self.request.POST)
        context['comments'] = Comment.objects.filter(confirm=True,
            course__slug=self.kwargs.get('slug'))
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
        # permit = True
        context['permit'] = permit
        context['wishlist'] = wishlist

        return context


class SearchView(ListView):
    model = Course
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        qs = None
        if request.GET:
            if request.GET.get("search_name"):
                qs = Course.objects.filter(Q(title__icontains=request.GET.get("search_name")) | 
                 Q(author__name__icontains=request.GET.get("search_name")))
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

    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated:
            return render(request,'404.html')
        return super().dispatch(request, *args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "confirm_delete_comment.html"

    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated:
            return render(request,'404.html')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteCommentView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self): 
        return reverse_lazy( 'single_courses', kwargs = {'slug':self.request.POST.get("course_slug", None) })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ErrorView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorListView(ListView):
    template_name = 'author-list.html'
    model = Author
    context_object_name = 'authors'
    paginate_by = 4


     
class AuthorDetailView (DetailView):
    model = Author
    template_name = 'author-detail.html'
    context_object_name = 'author'

    def get_success_url(self):
        return reverse_lazy('author-detail', kwargs = {'slug':self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_authors'] = Author.objects.filter(speciality=Author.objects.get(slug=self.kwargs.get('slug')).speciality).exclude(slug=self.kwargs.get('slug'))
        context['for_course_count'] = Author.objects.annotate(number_of_courses = Count("author_courses")).filter(slug=self.kwargs.get('slug')).first()

        return context


@login_required
def wishlist(request):
    courses = Course.objects.filter(users_wishlist=request.user)
    context = {
        "wishlist": courses
    }
    if request.user.is_authenticated:
        return render(request, "user_wish_list.html", context=context)
    return render(request, "404.html", context=context)


@login_required
def add_to_wishlist(request, id):
    course = get_object_or_404(Course, id=id)
    if course.users_wishlist.filter(id=request.user.id).exists():
        course.users_wishlist.remove(request.user)
        # messages.success(request, course.title + " bəyəndiklərim siyahısından silindi.")
    else:
        course.users_wishlist.add(request.user)
        # messages.success(request, course.title + " bəyəndiklərim siyahısına əlavə edildi.")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])