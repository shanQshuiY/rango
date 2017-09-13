# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

# Create your views here.

def index(request):
    #context_dic = {'boldmessage' : '"I am bold font from the context'}
    category_list = Category.objects.order_by('-likes')[:5]
    context_dic = {'categories': category_list}

    view_most_list = Page.objects.order_by('-views')[:5]
    context_dic['viewmost'] = view_most_list
    return render(request, 'rango/index.html', context_dic)

def about(request):
    context_dic = {}
    return render(request, 'rango/about.html', context_dic)

def category(request, category_name_slug):
    context_dic = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dic['category_name'] = category.name

        pages = Page.objects.filter(category=category)

        context_dic['pages'] = pages
        context_dic['category'] = category

    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dic)