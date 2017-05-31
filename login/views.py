# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render, redirect, get_object_or_404

from .models import Account

from .forms import LoginForm
def index(request):
    if request.session.has_key('username'):
        return render(request, 'login/logout.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            a = get_object_or_404(Account, username=u)
            if a.password == p:
                request.session.flush()
                request.session['username'] = a.username
                return render(request, 'login/logout.html')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    request.session.flush()
    return redirect('login:index')

