from django.views.generic import TemplateView, CreateView
from .forms import ContactForm
from django.urls import reverse_lazy
from core.models import HomeSettings
from courses.models import Comment


class HomeView(TemplateView):
    template_name = 'home.html'
    model = HomeSettings
    context_object_name = 'settings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting'] = HomeSettings.objects.filter(is_active=True).order_by('-created_at').first()
        context['landing_comments'] = Comment.objects.filter(confirm=True, in_landing=True)
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        context = super().form_valid(form)
        return context


# class SubscribeView(CreateView):
#     template_name = 'index.html'
#     form_class = SubscribeForm
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         result = super().form_valid(form)
#         return result