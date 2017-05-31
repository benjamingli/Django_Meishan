# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render, redirect, get_object_or_404
import subprocess, datetime, re, os

from .models import Task


def index(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    tasks = Task.objects.filter(user=u)
    return render(request, 'bhgj/index.html', {'tasks': tasks})

def detail(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    data = shell("/django/CODE/tree.py /var/www/upload/bhgj/%s.out" % t.id)
    return render(request, 'bhgj/detail.html', {'data': data, 'task': t})

def delete(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user == request.session['username']:
        shell("rm /var/www/upload/bhgj/%s.out" % t.id)
        shell("rm /var/www/upload/bhgj/%s.csv" % t.id)
        shell("rm /var/www/upload/bhgj/%s.reset.out" % t.id)
        shell("rm /var/www/upload/bhgj/%s.reset.csv" % t.id)
        shell("rm /var/www/upload/bhgj/%s" % t.fullname)
        t.delete()
    return redirect('bhgj:index')

def conf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    if request.method != 'POST':
        return render(request, 'bhgj/conf.html', {})

    upFile = request.FILES.get("upfile", None)
    if not upFile:
        return render(request, 'bhgj/conf.html', {'output': "无上传文件"})
    if not re.search(r'\.csv$', upFile.name):
        return render(request, 'bhgj/conf.html', {'output': "文件名后缀必须为.csv"})
    if re.search(r'[/\s\\]+', upFile.name):
        return render(request, 'bhgj/conf.html', {'output': "文件名不能包含空格、斜杠"})
    f = "%s-%s" % (u, upFile.name)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        old = Task.objects.get(fullname=f)
        return render(request, 'bhgj/conf.html', {'output': "文件已存在"})
    except ObjectDoesNotExist:
        pass

    try:
        hT = int(request.POST['hT'])
        dT = int(request.POST['dT'])
    except Exception:
        return render(request, 'bhgj/conf.html', {'output': "阈值为整数"})

    mydir = "/var/www/upload/bhgj"
    path = "%s/%s" % (mydir, f)
    destination = open(path.encode("utf8"), 'wb+')
    for chunk in upFile.chunks():
        destination.write(chunk)
    destination.close()
    output = "文件%s上传成功\n" % f

    timeNow = datetime.datetime.now()
    t = Task(user=u, time=timeNow, name=upFile.name, fullname=f, hourT=hT, dayT=dT)
    t.save()

    output += shell("/django/CODE/csv/codeFile.py %s %s/%s.csv2" % (path, mydir, t.id))
    output += shell("/django/CODE/csv/csvTrim.py %s/%s.csv2 %s/%s.csv" % (mydir, t.id, mydir, t.id))
    output += shell("rm %s/%s.csv2" % (mydir, t.id))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -put %s/%s.csv /app1/bhgj/" % (mydir, t.id))
    output += shell("/django/CODE/bhgj/resetTime.py %s/%s.csv %s/%s.reset.out" % (mydir, t.id, mydir, t.id))
    output += shell("/django/CODE/csv/codeFile2gbk.py %s/%s.reset.out %s/%s.reset.csv" % (mydir, t.id, mydir, t.id))
    output += shell("rm %s/%s.csv" % (mydir, t.id))

    inFile = "/app1/bhgj/%s.csv" % t.id
    outFile= "/app1/bhgj/%s.out" % t.id
    output += shell("/django/CODE/fis.pl /opt/spark/Spark/spark/bin/spark-submit /django/CODE/bhgj/Bhgj.jar %s %s %s %s" % (inFile, outFile, hT, dT))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -cat /app1/bhgj/%s.out/* > %s/%s.out" % (t.id, mydir, t.id))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/bhgj/%s.csv" % t.id)
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/bhgj/%s.out" % t.id)
    output += shell("/django/CODE/csv/codeFile2gbk.py %s/%s.out %s/%s.csv" % (mydir, t.id, mydir, t.id))

    return render(request, 'bhgj/conf.html', {'output': output})


def shell(order):
    p = subprocess.Popen(order.encode("utf8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    (out, err) = p.communicate()
    return out


def list(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    h = {}
    f = open("/var/www/upload/bhgj/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        r = re.match(r'^([^\s]+)\s', l[1])
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    data = ""
    for i in range(len(s)):
        data += "<tr><td>"+s[i]+"</td>\n<td>"
        data += '<a href="/bhgj/'+id_num+'/stat/'+str(i)+'/">查看</a></td>\n<td>'
        data += str(h[s[i]])+"</td></tr>\n"
    return render(request, 'bhgj/list.html', {'data': data, 'task': t})


def stat(request, id_num, name):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    h = {}
    f = open("/var/www/upload/bhgj/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        r = re.match(r'^([^\s]+)\s', l[1])
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    target = s[int(name)]
    data = ""
    f = open("/var/www/upload/bhgj/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        if l[1].find(target) != -1:
            data += "<tr><td>"
            data += "</td><td>".join(l)
            data += "</td></tr>\n"
    f.close()
    return render(request, 'bhgj/stat.html', {'data': data, 'task': t})


def reset(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    data = ""
    count = 0
    f = open("/var/www/upload/bhgj/%s.reset.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        count += 1
        if count > 500: break
        l = line.strip().split(',')
        data += "<tr><td>"
        data += "</td><td>".join(l)
        data += "</td></tr>\n"
    f.close()
    return render(request, 'bhgj/reset.html', {'data': data, 'task': t})

def relist(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    h = {}
    f = open("/var/www/upload/bhgj/%s.reset.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        r = re.match(r'^([^\s]+)\s', l[2])
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    data = ""
    for i in range(len(s)):
        data += "<tr><td>"+s[i]+"</td>\n<td>"
        data += '<a href="/bhgj/'+id_num+'/reset/stat/'+str(i)+'/">查看</a></td>\n<td>'
        data += str(h[s[i]])+"</td></tr>\n"
    return render(request, 'bhgj/list.html', {'data': data, 'task': t})


def restat(request, id_num, name):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('bhgj:index')
    h = {}
    f = open("/var/www/upload/bhgj/%s.reset.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        r = re.match(r'^([^\s]+)\s', l[2])
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    target = s[int(name)]
    data = ""
    f = open("/var/www/upload/bhgj/%s.reset.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        if l[2].find(target) != -1:
            data += "<tr><td>"
            data += "</td><td>".join(l)
            data += "</td></tr>\n"
    f.close()
    return render(request, 'bhgj/restat.html', {'data': data, 'task': t})


