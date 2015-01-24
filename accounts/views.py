# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from accounts.forms import UserForm, UserProfileForm
from django.contrib import messages


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, u'حساب کاربری شما غیرفعال می‌باشد.')
                return render_to_response('accounts/accounts_login.html', {}, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            messages.error(request, u'نام کاربری یا رمز عبور اشتباه می‌باشد.')
            return render_to_response('accounts/accounts_login.html', {}, context)
    else:
        return render_to_response('accounts/accounts_login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'accounts/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)
