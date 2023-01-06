from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from start.models import Profile
from .forms import RememberModelForm
from .models import RememberModel


def get_profile_data_by_user(user):
    try:
        return Profile.objects.get(user=user)
    except:
        raise ValueError("Такой пользователь не найден")


@login_required
def index(request):
    profile = get_profile_data_by_user(request.user)
    remembers = RememberModel.objects.all().filter(profile=profile)
    context = profile.get_name_and_avatar()
    context['remembers'] = remembers
    return render(request, 'user_impressions/index.html',
                  context)


class CreateRememberView(View):
    def get(self, request):
        context = get_profile_data_by_user(request.user).get_name_and_avatar()
        context['form'] = RememberModelForm()
        return render(request, 'user_impressions/form.html',
                      context)

    def post(self, request):
        bound_form = RememberModelForm(request.POST)
        profile = get_profile_data_by_user(request.user)
        if bound_form.is_valid():
            bound_form.save_form(profile)
            return redirect('home')
        context = profile.get_name_and_avatar()
        context['form'] = bound_form
        return render(request, 'user_impressions/form.html',
                      context)


def details(request, slug):
    profile = get_profile_data_by_user(request.user)
    remember = RememberModel.objects.get(slug__iexact=slug)
    context = profile.get_name_and_avatar()
    context['remember'] = remember
    return render(request, 'user_impressions/details.html', context)


def remember_delete(request, slug):
    profile = get_profile_data_by_user(request.user)
    remember = RememberModel.objects.get(profile=profile, slug__iexact=slug)
    remember.delete()
    return redirect("home")
