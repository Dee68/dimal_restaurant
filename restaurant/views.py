from django.shortcuts import render

# Create your views here.


def restaurant_list(request):
    return render(request, 'restaurant/restaurant_list.html')


def restaurant_detail(request, id, slug):
    return render(request, 'restaurant/restaurant_detail.html')