from django.views.generic import TemplateView, CreateView
from .forms import ContactForm 
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    # success_message = "%(name)s was created successfully"
    def form_valid(self, form):
        context = super().form_valid(form)
        return context