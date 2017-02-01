from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from graphs.models import Attendance, Notes, Tests
from django.core import serializers
from django import forms	#may not need
from django.db import connection
import numpy as np
import json
import time
import math
import datetime
from datetime import timedelta
from datetime import date

# Create your views here.
def gpfront(request):
    return render(request, 'GP/gpfront.html')
	
def costfront(request):
    return render(request, 'GP/costfront.html')
	
def costs_bubble(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    loca=request.GET.get('loca', 'M83032')
    view=request.GET.get('view', 'spend')
    cursor=connection.cursor()
    cursor.execute("SELECT set_code, set_exp, COUNT(DISTINCT specimen_number), (SELECT MAX(convert(float, standard_cat_c)) FROM cost c WHERE c.set_code=t.set_code AND c.Discipline=t.discipline) FROM gptests t WHERE datereceived BETWEEN convert(date, %s )     AND convert(date, %s )     and location = %s GROUP BY set_code,t.discipline,    set_exp", [start, end, loca])
    raw_data=cursor.fetchall()
    cursor.execute("select location, unit_location_group_exp, location_exp, count(*) from gptests t join location l on t.location=l.location_code where unit_location_group_exp in ('Birm East and North PCT','Heart of Birmingham PCT','Solihull PCT','South Birmingham PCT','South Staffordshire PCT','Walsall Teaching PCT','Warwickshire PCT') group by location,  unit_location_group_exp, location_exp having count(*)>100 order by location")
    locations=cursor.fetchall()
    locs=[row[0] for row in locations]
    loc_exp=[row[2] for row in locations if row[0] == loca]
    data={}
    sets=[(row[0],row[1]) for row in raw_data]
    for row in raw_data:
        data[row[0]]={'set_code':row[0], 'set_exp':row[1], 'count':row[2], 'cost':row[3]}
    data2=json.dumps(data)
    return render(request, 'GP/cost_bubble.html', {'data':data2, 'test':'test', 'start':start, 'end':end, 'view':view, 'setexp':sets, 'locs':locs, 'loca':loca, 'loc_exp':loc_exp})
	
def costxgp(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    set=request.GET.get('set', "UE")
    view=request.GET.get('view', "Standardised Request Count")
    cursor=connection.cursor()
    cursor.execute("select distinct set_code, set_exp from gptests t join location on location=location_code where num_of_pts>0 order by set_exp")
    loc_data=cursor.fetchall()
    set_list=[(row[0],row[1]) for row in loc_data]
    if set=='tumour':
        cursor.execute("select location_code, location_exp, num_of_pts, count(*) as test_count, unit_location_group_exp from location l join gptests g on l.location_code=g.location where num_of_pts>0 and datereceived BETWEEN convert(date, %s) AND convert(date, %s) and set_code in ('CEA', 'CA125', 'CA153', 'CA199R', 'AFP', 'PSA', 'HCGTM') group by location_code, location_exp, num_of_pts, unit_location_group_exp", [start, end])
        set_exp='Tumour Markers'
    else:
        cursor.execute("select location_code, location_exp, num_of_pts, count(*) as test_count, unit_location_group_exp from location l join gptests g on l.location_code=g.location where num_of_pts>0 and datereceived BETWEEN convert(date, %s) AND convert(date, %s) and set_code = %s group by location_code, location_exp, num_of_pts, unit_location_group_exp", [start, end, set])
        set_exp=[row[1] for row in loc_data if row[0]==set][0]
    raw_data=cursor.fetchall()
    data={}
    for row in raw_data:
        data[row[0]]={'loc_code':row[0], 'loc_exp':row[1], 'pt_count':row[2], 'set_count':row[3], 'norm_val':float(row[3])/row[2]}
    data2=json.dumps(data)
    return render(request, 'GP/costxgp.html', {'start':start, 'end':end, 'view':view, 'set':set, 'set_list':set_list, 'set_exp':set_exp, 'data':data2})
	
def ice_front(request):
    return render(request, 'GP/ice_front.html')	

def ice_by_location(request):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    return render(request, 'GP/ice_by_gp.html')
	
def r_front(request):
    return render(request, 'GP/r_front.html')

def r_by_location(request):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    location=request.GET.get('loca', 'M85741')
    cursor=connection.cursor()
    cursor.execute("select location, set_code, set_exp, consultant, count(*) from gptests g WHERE datereceived BETWEEN convert(date, %s ) AND convert(date, %s ) and location =%s AND set_code not in ('PROBL', 'SEND', 'SI') group by location, set_code, set_exp, consultant", [start, end, location])
    raw_data=cursor.fetchall()
    cursor.execute("select location_code, location_exp from location l join gptests g on g.location=l.location_code where num_of_pts>0 group by  location_code, location_exp having count(*)>100 order by location_exp")
    loc_list=cursor.fetchall()
    data={}
    set_codes=list(set([row[1] for row in raw_data]))
    con_codes=list(set([row[3] for row in raw_data]))
    loc_exp=[row[1] for row in loc_list if location==row[0]][0]
    for set_code in set_codes:
        data[set_code]={}
        data[set_code]['set_exp']=[row[2] for row in raw_data if row[1]==set_code][0]
        data[set_code]['total_count']=sum([row[4] for row in raw_data if row[1]==set_code])
        for con in con_codes:
            data[set_code][con]=sum([row[4] for row in raw_data if row[1]==set_code and row[3]==con])
    data2=json.dumps(data)
    return render(request, 'GP/level_by_location.html', {'start':start, 'end':end, 'data':data2, 'loc_list':loc_list, 'location':location, 'loc_exp':loc_exp, 'con_codes':con_codes})	

def boxplots_set_by_loc(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    location=request.GET.get('loca', 'M85741')
    view=request.GET.get('view', "Patients at Practice")
    cursor=connection.cursor()
    cursor.execute("select location_code, location_exp from location l join gptests g on g.location=l.location_code where num_of_pts>0 group by  location_code, location_exp having count(*)>100 order by location_exp")
    loc_list=cursor.fetchall()
    cursor.execute("SELECT location_code, location_exp, set_code, set_exp, num_of_pts, COUNT(*) AS test_count, unit_location_group_exp FROM location l join gptests g ON l.location_code=g.location WHERE num_of_pts>0 AND datereceived BETWEEN convert(date, %s) AND convert(date, %s) AND set_code not in ('PROBL', 'SEND', 'SI') GROUP BY location_code, location_exp, num_of_pts, unit_location_group_exp, set_code, set_exp order by location_exp", [start, end])
    raw_data=cursor.fetchall()
    set_codes=set([row[2] for row in raw_data])
    loc_exp=[row[1] for row in loc_list if row[0]==location]
    num_locs=len(set([row[0] for row in raw_data]))
    data={}
    for set_code in set_codes:
        data[set_code]={}
        data[set_code]['count']=[row[5] for row in raw_data if row[2]==set_code]
        data[set_code]['count']=data[set_code]['count']+[0 for i in range(num_locs-len(data[set_code]['count']))]
        data[set_code]['norm_count']=[float(row[5])/row[4] for row in raw_data if row[2]==set_code]
        data[set_code]['norm_count']=data[set_code]['norm_count']+[0 for i in range(num_locs-len(data[set_code]['norm_count']))]
        data[set_code]['loc_value']=[row[5] for row in raw_data if row[2]==set_code and row[0]==location]
        data[set_code]['norm_loc_value']=[float(row[5])/row[4] for row in raw_data if row[2]==set_code and row[0]==location]
    data2=json.dumps(data)
    return render(request, 'GP/boxplots_set_by_loc.html', {'data':data2, 'num_locs':num_locs, 'start':start, 'end':end, 'loc_list':loc_list, 'loca':location, 'loc_exp':loc_exp})
	
	
	
	
	
	
	
	