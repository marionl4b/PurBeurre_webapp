from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f"Votre compte vient d'être créé !, "
                             f"vous pouvez désormais vous connecter")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)


@login_required
def profile(request):
    return render(request, 'website/profile.html')