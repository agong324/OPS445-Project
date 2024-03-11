#users/signup.py

from django.contrib import messages

def signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You are now registered!")
            return redirect('core:home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})
