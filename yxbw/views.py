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
    return render(request, 'yxbw/index.html', {'tasks': tasks})

def detail(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('yxbw:index')
    data = ""
    count = 0
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        count += 1
        if count > 150: break
        l = line.strip().split(',')
        if count % 2 == 1:
            data += "<tr>"
        data += "<td>"
        data += "</td><td>".join(l)
        data += "</td>"
        if count % 2 == 0:
            data += "</tr>\n"
    f.close()
    return render(request, 'yxbw/detail.html', {'data': data, 'task': t})

def delete(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user == u:
        shell("rm /var/www/upload/yxbw/%s.out" % t.id)
        shell("rm /var/www/upload/yxbw/%s.csv" % t.id)
        shell("rm /var/www/upload/yxbw/%s" % t.fullname)
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/yxbw/%s_%s.csv" % (u, t.id))
        t.delete()
    return redirect('yxbw:index')

def conf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    if request.method != 'POST':
        return render(request, 'yxbw/conf.html', {})

    upFile = request.FILES.get("upfile", None)
    if not upFile:
        return render(request, 'yxbw/conf.html', {'output': "无上传文件"})
    if not re.search(r'\.csv$', upFile.name):
        return render(request, 'yxbw/conf.html', {'output': "文件名后缀必须为.csv"})
    if re.search(r'[/\s\\]+', upFile.name):
        return render(request, 'yxbw/conf.html', {'output': "文件名不能包含空格、斜杠"})
    f = "%s-%s" % (u, upFile.name)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        old = Task.objects.get(fullname=f)
        return render(request, 'yxbw/conf.html', {'output': "文件已存在"})
    except ObjectDoesNotExist:
        pass

    acc = False
    if request.POST.has_key('accum') and request.POST['accum']:
        acc = True

    mydir = "/var/www/upload/yxbw"
    path = "%s/%s" % (mydir, f)
    destination = open(path.encode("utf8"), 'wb+')
    for chunk in upFile.chunks():
        destination.write(chunk)
    destination.close()
    output = "文件%s上传成功\n" % f

    timeNow = datetime.datetime.now()
    t = Task(user=u, time=timeNow, name=upFile.name, fullname=f, accum=acc)
    t.save()

    if u == "root":
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1")
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1/load")
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1/yxbw")
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1/ycyx")
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1/bhgj")
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -mkdir /app1/gpxx")

    output += shell("/django/CODE/csv/codeFile.py %s %s/%s.csv2" % (path, mydir, t.id))
    output += shell("/django/CODE/csv/csvTrim.py %s/%s.csv2 %s/%s_%s.csv" % (mydir, t.id, mydir, u, t.id))
    output += shell("rm %s/%s.csv2" % (mydir, t.id))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -put %s/%s_%s.csv /app1/yxbw/" % (mydir, u, t.id))
    output += shell("rm %s/%s_%s.csv" % (mydir, u, t.id))

    if acc:
        inFile = "/app1/yxbw/%s_*.csv" % u
    else:
        inFile = "/app1/yxbw/%s_%s.csv" % (u, t.id)
    outFile= "/app1/yxbw/%s.out" % t.id
    output += shell("/django/CODE/fis.pl /opt/spark/Spark/spark/bin/spark-submit /django/CODE/yxbw/Yxbw.jar %s %s" % (inFile, outFile))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -cat /app1/yxbw/%s.out/* > %s/%s.out" % (t.id, mydir, t.id))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/yxbw/%s.out" % t.id)
    output += shell("/django/CODE/csv/codeFile2gbk.py %s/%s.out %s/%s.csv" % (mydir, t.id, mydir, t.id))

    return render(request, 'yxbw/conf.html', {'output': output})


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
        return redirect('yxbw:index')
    h = {}
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        r = re.match(r'^([^\s]+)\s', line)
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    data = ""
    for i in range(len(s)):
        if s[i].find("FAIL") == -1:
            data += "<tr><td>"+s[i]+"</td>\n<td>"
            data += '<a href="/yxbw/'+id_num+'/stat/'+str(i)+'/">查看</a></td>\n<td>'
            data += str(h[s[i]])+"</td></tr>\n"
    return render(request, 'yxbw/list.html', {'data': data, 'task': t})


def stat(request, id_num, name):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('yxbw:index')
    h = {}
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        r = re.match(r'^([^\s]+)\s', line)
        cz = r.group(1)
        if h.has_key(cz):
            h[cz] += 1
        else:
            h[cz] = 1
    f.close()
    s = sorted(h.keys())
    target = s[int(name)]
    data = ""
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')
        if l[0].find(target) != -1:
            data += "<tr><td>"
            data += "</td><td>".join(l)
            data += "</td></tr>\n"
    f.close()
    return render(request, 'yxbw/stat.html', {'data': data, 'task': t})


def kg(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('yxbw:index')
    data = ""
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        if line.find(u"开关")!=-1 and line.find(u"刀闸")==-1 and line.find(u"地刀")==-1:
            l = line.strip().split(',')
            data += "<tr><td>"
            data += "</td><td>".join(l)
            data += "</td></tr>\n"
    f.close()
    return render(request, 'yxbw/kgdz.html', {'data': data, 'task': t})

def dz(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    t = get_object_or_404(Task, pk=int(id_num))
    if t.user != request.session['username']:
        return redirect('yxbw:index')
    data = ""
    f = open("/var/www/upload/yxbw/%s.out" % t.id)
    while True:
        line = f.readline()
        if not line: break
        if line.find(u"刀闸")!=-1 or line.find(u"地刀")!=-1:
            l = line.strip().split(',')
            data += "<tr><td>"
            data += "</td><td>".join(l)
            data += "</td></tr>\n"
    f.close()
    return render(request, 'yxbw/kgdz.html', {'data': data, 'task': t})


