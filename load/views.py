# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
import subprocess, datetime, re, os

from .models import Weather, RawCsv, Data, Result


def index(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    return render(request, 'load/index.html', {})


def weather(request, year="0", month="0"):
    if not request.session.has_key('username'):
        return redirect('login:index')
    if year=="0" and month=="0":
        today = datetime.date.today()
        year = "%d" % today.year
        month = "%d" % today.month
    start = datetime.date(int(year), int(month), 1)
    from datetime import timedelta
    from calendar import monthrange
    end = start + timedelta(days=monthrange(start.year,start.month)[1]-1)
    weathers = Weather.objects.filter(date__range=(start, end))
    return render(request, 'load/weather.html', {'weathers': weathers})

def weatherDel(request, year, month, day):
    if not request.session.has_key('username'):
        return redirect('login:index')
    d = datetime.date(int(year), int(month), int(day))
    w = get_object_or_404(Weather, date=d)
    w.delete()
    return redirect(reverse('load:weather', args=[year, month]))

from .forms import WeatherForm
def weatherConf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data['date']
            h = 1 if form.cleaned_data['holiday'] else 0
            try:
                maxT = int(float(form.cleaned_data['maxTemp']))
                minT = int(float(form.cleaned_data['minTemp']))
                t    = int(form.cleaned_data['typeDay'])
            except:
                output = "气温必须为数字"
                return render(request, 'load/weatherConf.html', {'form': form, 'output': output})
            from django.core.exceptions import ObjectDoesNotExist
            try:
                old = Weather.objects.get(date=d)
                old.delete()
                output = "更新记录:"
            except ObjectDoesNotExist:
                output = "创建记录:"
            w = Weather(date=d, holiday=h, maxTemp=maxT, minTemp=minT, typeDay=t)
            w.save()
            output += " %s,%s,%s,%s,%s 成功!" % (d, h, maxT, minT, t)
            return render(request, 'load/weatherConf.html', {'form': form, 'output': output})
    else:
        form = WeatherForm()
    return render(request, 'load/weatherConf.html', {'form': form})


def rawCsv(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    rawCsvs = RawCsv.objects.filter(user=u)
    return render(request, 'load/rawCsv.html', {'rawCsvs': rawCsvs})

def rawCsvDel(request, fullname):
    if not request.session.has_key('username'):
        return redirect('login:index')
    r = get_object_or_404(RawCsv, fullname=fullname)
    if r.user == request.session['username']:
        r.delete()
        shell("rm /var/www/upload/load/%s" % fullname)
    return redirect('load:rawCsv')

def rawCsvConf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    if request.method != 'POST':
        return render(request, 'load/rawCsvConf.html', {})

    upFile = request.FILES.get("upfile", None)
    if not upFile:
        return render(request, 'load/rawCsvConf.html', {'output': "无上传文件"})

    m = re.match(r'^(.+)\.(csv)$', upFile.name)
    if not m:
        return render(request, 'load/rawCsvConf.html', {'output': "文件名后缀必须为.csv"})
    n = m.group(1)
    t = m.group(2)
    if re.search(r'[/\s\\]+', n):
        return render(request, 'load/rawCsvConf.html', {'output': "文件名不能包含空格、斜杠"})

    f = "%s-%s.csv" % (u, n)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        old = RawCsv.objects.get(fullname=f)
        return render(request, 'load/rawCsvConf.html', {'output': "文件已存在"})
    except ObjectDoesNotExist:
        pass

    mydir = "/var/www/upload/load/"
    path = "%s%s-%s" % (mydir, u, upFile.name)
    destination = open(path.encode("utf8"), 'wb+')
    for chunk in upFile.chunks():
        destination.write(chunk)
    destination.close()
    output = "文件%s上传成功\n" % path

    p = "%s%s-%s" % (mydir, u, n)
    if t=='xls' or t=='xlsx':
        output += shell("in2csv %s > %s.csv2" % (path, p))
        output += shell("rm %s" % path)
        output += shell("/django/CODE/csv/csvTrim.py %s.csv2 %s.csv" % (p, p))
        output += shell("rm %s.csv2" % p)
    if t=='csv':
        output += shell("/django/CODE/csv/codeFile.py %s %s.csv2" % (path, p))
        output += shell("/django/CODE/csv/csvTrim.py %s.csv2 %s" % (p, path))
        output += shell("rm %s.csv2" % p)
    output += "文件格式转换成功\n"

    timeNow = datetime.datetime.now()
    r = RawCsv(user=u, time=timeNow, filename="%s.csv" % n, fullname=f)
    r.save()
    return render(request, 'load/rawCsvConf.html', {'output': output})


def data(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    datas = Data.objects.filter(user=u)
    return render(request, 'load/data.html', {'datas': datas})

def dataDel(request, fullname):
    if not request.session.has_key('username'):
        return redirect('login:index')
    d = get_object_or_404(Data, fullname=fullname)
    if d.user == request.session['username']:
        shell("rm /var/www/upload/load/%s.name" % fullname)
        shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s" % fullname)
        d.delete()
    return redirect('load:data')

def dataConf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    rawCsvs = RawCsv.objects.filter(user=u)
    if request.method != 'POST':
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs})
    n = request.POST['name']
    if n == "":
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': "模型名称不能为空"})
    if re.search(r'[^\w\.\_]+', n):
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': "模型名称只能包含数字、字母和下划线"})
    if re.search(r'\.csv$', n):
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': "模型名称后缀不能为.csv"})
    f = "%s-%s" % (u, n)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        old = Data.objects.get(fullname=f)
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': "模型名已存在"})
    except ObjectDoesNotExist:
        pass

    output = "读取文件:\n"
    paramIn = ""
    for csv in RawCsv.objects.filter(user=u):
        if request.POST.has_key(str(csv.id)) and request.POST[str(csv.id)]:
            output += "%s\n" % csv.filename
            paramIn += " /var/www/upload/load/%s" % csv.fullname
    if paramIn == "":
        return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': "未选取文件"})

    output += shell("/django/CODE/load/trainData.py /var/www/upload/load/%s%s" % (f, paramIn))
    output += "生成数据成功\n上传数据至hdfs\n"
    shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s" % f)
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -put /var/www/upload/load/%s /app1/load/" % f)
    output += shell("rm /var/www/upload/load/%s" % f)

    timeNow = datetime.datetime.now()
    d = Data(user=u, time=timeNow, filename=n, fullname=f)
    d.save()

    return render(request, 'load/dataConf.html', {'rawCsvs': rawCsvs, 'output': output})


def result(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    results = Result.objects.filter(user=u)
    return render(request, 'load/result.html', {'results': results})

def resultDetail(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    r = get_object_or_404(Result, pk=int(id_num))
    if r.user != request.session['username']:
        return redirect('load:result')
    pngs = []
    for i in range(r.n):
        pngs.append("/upload/load/%s_%03d.png" % (r.prefix, i))
    return render(request, 'load/resultDetail.html', {'result': r, 'pngs': pngs})

def resultDel(request, id_num):
    if not request.session.has_key('username'):
        return redirect('login:index')
    r = get_object_or_404(Result, pk=int(id_num))
    if r.user == request.session['username']:
        shell("rm /var/www/upload/load/%s*" % r.prefix)
        r.delete()
    return redirect('load:result')

from .forms import ResultForm
def resultConf(request):
    if not request.session.has_key('username'):
        return redirect('login:index')
    u = request.session['username']
    datas = Data.objects.filter(user=u)
    if request.method != 'POST':
        form = ResultForm()
        return render(request, 'load/resultConf.html', {'datas': datas, 'form': form})
    form = ResultForm(request.POST)
    if not form.is_valid():
        return render(request, 'load/resultConf.html', {'datas': datas, 'form': form})
    if not request.POST.has_key('data'):
        return render(request, 'load/resultConf.html', {'datas': datas, 'form': form, 'output': '未选取模型'})
    d = form.cleaned_data['date']
    from django.core.exceptions import ObjectDoesNotExist
    try:
        w = Weather.objects.get(date=d)
    except ObjectDoesNotExist:
        return render(request, 'load/resultConf.html', {'datas': datas, 'form': form, 'output': '请设置当日天气'})

    m = get_object_or_404(Data, pk=int(request.POST['data']))
    output = "读取模型:%s\n" % m.filename
    num = int(shell("cat /var/www/upload/load/%s.name|wc -l" % m.fullname))
    day = d.strftime('%Y-%m-%d')
    weatherStr = "%s,%s,%s,%s" % (w.holiday, w.maxTemp, w.minTemp, w.typeDay)
    predData = "%s.%s" % (m.fullname, d.strftime('%Y%m%d'))
    output += shell("/django/CODE/load/predictData.py %s %s %s /var/www/upload/load/%s" % (num, day, weatherStr, predData))
    shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s" % predData)
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -put /var/www/upload/load/%s /app1/load/" % predData)
    output += shell("rm /var/www/upload/load/%s" % predData)

    dataFile = "/app1/load/%s" % m.fullname
    predFile = "/app1/load/%s" % predData
    outFile  = "/app1/load/%s.out" % predData
    shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s.out" % predData)
    output += "模型预测\n"
    output += shell("/django/CODE/fis.pl /opt/spark/Spark/spark/bin/spark-submit /django/CODE/load/Load.jar %s %s %s %s" % (num, dataFile, predFile, outFile))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -cat /app1/load/%s.out/* > /var/www/upload/load/%s.out" % (predData, predData))
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s" % predData)
    output += shell("/django/CODE/fi.pl /opt/hdfs/HDFS/hadoop/bin/hadoop fs -rm -r /app1/load/%s.out" % predData)

    shell("rm /var/www/upload/load/%s.res*" % predData)
    output += shell("/django/CODE/load/drawData.py /var/www/upload/load/%s.name /var/www/upload/load/%s.out /var/www/upload/load/%s.res" % (m.fullname, predData, predData))
    output += shell("rm /var/www/upload/load/%s.out" % predData)

    resPath = "/var/www/upload/load/%s.res" % predData
    output += shell("/django/CODE/csv/codeFile2gbk.py %s.csv %s.csv2" % (resPath, resPath))
    output += shell("mv %s.csv2 %s.csv" % (resPath, resPath))

    timeNow = datetime.datetime.now()
    r = Result(user=u, time=timeNow, data=m.filename, date=d, prefix="%s.res" % predData, n=num)
    r.save()

    return render(request, 'load/resultConf.html', {'datas': datas, 'form': form, 'output': output})


def shell(order):
    p = subprocess.Popen(order.encode("utf8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    (out, err) = p.communicate()
    return out
