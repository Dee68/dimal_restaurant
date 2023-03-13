from django.shortcuts import render

# Create your views here.


def restaurant(request):
    return render(request, 'restaurant/index.html')


def restaurant_detail(request, id, slug):
    return render(request, 'restaurant/restaurant_detail.html')