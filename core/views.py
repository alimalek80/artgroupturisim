from django.shortcuts import render


def home_view(request):
    """
    Homepage view displaying welcome content and featured tours.
    """
    context = {
        'page_title': 'Welcome to Art Tourism',
    }
    return render(request, 'core/home.html', context)
