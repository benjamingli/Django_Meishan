# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import redirect

def index(request):
    return redirect('login:index')
