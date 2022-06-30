from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem


def calculate():
    x = 1
    y = 2
    return x


def say_hello(request):
    
    query_set = Product.objects.filter(id__in = OrderItem.objects.values('product_id').distinct()).order_by('title')

    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(query_set)})
 