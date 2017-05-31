# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render, redirect
import socket, string, subprocess

def index(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    ip = socket.gethostbyname(socket.gethostname())
    if string.atoi(shell("ps uax|grep hadoop|wc -l")) > 2:
        hadoop = 1
    else:
        hadoop = 0
    if string.atoi(shell("ps uax|grep spark|wc -l")) > 2:
        spark = 1
    else:
        spark = 0
    return render(request, 'cluster/index.html', {'ip': ip, 'hadoop': hadoop, 'spark': spark})

def hadoopOn(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    ip = socket.gethostbyname(socket.gethostname())

    output = "============启动HADOOP============\n"
    output += shell("expect /django/CODE/cluster/hadoopOn.sh")
    output += "============启动完成============\n"

    if string.atoi(shell("ps uax|grep hadoop|wc -l")) > 2:
        hadoop = 1
    else:
        hadoop = 0
    if string.atoi(shell("ps uax|grep spark|wc -l")) > 2:
        spark = 1
    else:
        spark = 0
    return render(request, 'cluster/index.html', {
        'ip': ip,
        'hadoop': hadoop,
        'spark': spark,
        'output': output})

def hadoopOff(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    ip = socket.gethostbyname(socket.gethostname())

    output = "============关闭HADOOP============\n"
    output += shell("expect /django/CODE/cluster/hadoopOff.sh")
    output += "============完成============\n"

    if string.atoi(shell("ps uax|grep hadoop|wc -l")) > 2:
        hadoop = 1
    else:
        hadoop = 0
    if string.atoi(shell("ps uax|grep spark|wc -l")) > 2:
        spark = 1
    else:
        spark = 0
    return render(request, 'cluster/index.html', {
        'ip': ip,
        'hadoop': hadoop,
        'spark': spark,
        'output': output})

def sparkOn(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    ip = socket.gethostbyname(socket.gethostname())

    output = "============启动SPARK============\n"
    output += shell("expect /django/CODE/cluster/sparkOn.sh")
    output += "============启动完成============\n"

    if string.atoi(shell("ps uax|grep hadoop|wc -l")) > 2:
        hadoop = 1
    else:
        hadoop = 0
    if string.atoi(shell("ps uax|grep spark|wc -l")) > 2:
        spark = 1
    else:
        spark = 0
    return render(request, 'cluster/index.html', {
        'ip': ip,
        'hadoop': hadoop,
        'spark': spark,
        'output': output})

def sparkOff(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    ip = socket.gethostbyname(socket.gethostname())

    output = "============关闭SPARK============\n"
    output += shell("expect /django/CODE/cluster/sparkOff.sh")
    output += "============完成============\n"

    if string.atoi(shell("ps uax|grep hadoop|wc -l")) > 2:
        hadoop = 1
    else:
        hadoop = 0
    if string.atoi(shell("ps uax|grep spark|wc -l")) > 2:
        spark = 1
    else:
        spark = 0
    return render(request, 'cluster/index.html', {
        'ip': ip,
        'hadoop': hadoop,
        'spark': spark,
        'output': output})

def shell(order):
    p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    (out, err) = p.communicate()
    return out
