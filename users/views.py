from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm


# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('main:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
