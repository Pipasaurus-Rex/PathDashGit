from django.shortcuts import render, HttpResponse
from front_page.models import Attendance, Notes, Tests
from django.db import connection

def front_page(request):
    cursor=connection.cursor()
    cursor.execute("select sum(case when specimen_taken_by is null then 0 when specimen_taken_by='' then 0 else 1 end) as ice_count, count(*) as [count] from tests where consultant in ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') and datepart(MM, datereceived) = datepart(MM, getdate()) and datepart(yyyy, datereceived) = datepart(yyyy, getdate())")	
    raw_data=cursor.fetchall()
    ice_percent=raw_data[0][0]*100/raw_data[0][1]
    return render(request, 'front_page/front_screen.html', {'ice_percent':ice_percent})
	
def addon_front(request):
    return render(request, 'front_page/Addons_front.html')

def repeats_front(request):
    return render(request, 'front_page/repeats_front.html')

def timeflow_front(request):
    return render(request, 'front_page/timeflow.html')
	
def req_levels_front(request):
    return render(request, 'front_page/rlevelsfront.html')
	
def new_devs(request):
    return render(request, 'front_page/new_developments.html')
	
def costs(request):
    return render(request, 'front_page/costs_front.html')

def ice(request):
    return render(request, 'front_page/ice_front.html')

def bundles_front(request):
    return render(request, 'front_page/bundles_front.html')
	
def test(request):
    return HttpResponse('BLARG!!')