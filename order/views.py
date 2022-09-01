from django.shortcuts import render

# Create your views here.

def card(request):
    context = {
        'title': 'Card Sellshop'
    }
    return render(request, "cart.html",context=context)
