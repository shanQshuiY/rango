# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render
from rango.models import Category, Page, UserProfile, User
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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
        context_dic['category_slug'] = category.slug
        context_dic['category'] = category

    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dic)

@login_required
def add_category(request):

    if (request.method == 'POST'):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            return form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.save()
                return  category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dic = {'category_slug' : category_name_slug}
    context_dic['form'] = form
    return render(request, 'rango/add_page.html', context_dic)


def register(request):

    registered = False
    context_dic = {}
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            print 'save pic'
            registered = True
            print registered
        else:
            print user_form.errors, profile_form.errors

    else:

        user_form = UserForm()
        context_dic['user_form'] = user_form
        profile_form = UserProfileForm()
        context_dic['profile_form'] = profile_form
    context_dic['registered'] = registered

    return render(request, 'rango/register.html', context_dic)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                #return render(request, '/rango/', {'user': user})
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled.')

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')