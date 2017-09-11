# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context_dic = {'boldmessage' : '"I am bold font from the context'}
    return render(request, 'rango/index.html', context_dic)
