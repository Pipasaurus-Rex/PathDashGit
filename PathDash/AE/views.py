from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from AE.models import Attendance, Notes, Tests
from django.core import serializers
from django import forms	#may not need
from django.db import connection
import json
import time
import math
import datetime
from datetime import timedelta
from datetime import date

def graphs_front(request):
    return render(request, 'graphs/graphs_front.html')
	
def addons(request):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    mins=request.GET.get('mins', 240)
    cursor=connection.cursor()
    cursor.execute("select set_code, set_exp, count(*) as count, avg(datediff(mi, datereceived, datebookedin)) as mean, var(datediff(mi, datereceived, datebookedin)), (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=t.set_code and Discipline!='I') as cost_per_test from tests t where datebookedin>(select min(datebookedin) from tests t1 where t1.specimen_number=t.specimen_number) and set_code not in ('PROBL', 'BHH')  AND datecollected between convert(date, %s ) and convert(date, %s ) and datediff(mi, datereceived, datebookedin)>%s and consultant in ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') group by set_code, set_exp", [start, end , mins])
    test=cursor.fetchall()
    data={}
    for i in test:
        t={i[0]:{'test':i[0],'test_exp':i[1],'count':i[2],'mean':i[3],'variance':i[4], 'costpertest':i[5]}}
        data.update(t)
    data2=json.dumps(data)
    cursor.close()
    return render(request, 'graphs/addon_graph.html', {'data':data2, 'start':start, 'end':end, 'mins':mins})
	
def addon_test_detail(request):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    set=request.GET.get('set', 'UE')
    cursor=connection.cursor()
    cursor.execute("select distinct set_code from tests order by set_code")
    raw_set_list=cursor.fetchall()
    set_list=[row[0] for row in raw_set_list]
    if set=="All":
        cursor.execute("SELECT set_exp, datediff(mi, episodedate, datebookedin) as timediff, timeinae, attendingclinician, dischargetype, consultantcode,  DiagnosisDescription1, diagnosiscode1 from tests t join attendance a on a.attendanceno=t.attendanceno WHERE datebookedin>( SELECT MIN(datebookedin) FROM tests t1 WHERE t1.specimen_number=t.specimen_number) AND datecollected between convert(date, %s ) and convert(date, %s ) ", [start, end])
    else:
        cursor.execute("SELECT set_exp, datediff(mi, episodedate, datebookedin) as timediff, timeinae, attendingclinician, dischargetype, consultantcode,  DiagnosisDescription1, diagnosiscode1 from tests t join attendance a on a.attendanceno=t.attendanceno WHERE datebookedin>( SELECT MIN(datebookedin) FROM tests t1 WHERE t1.specimen_number=t.specimen_number) and set_code= %s AND datecollected between convert(date, %s ) and convert(date, %s )", [set, start, end])
    raw_data=cursor.fetchall()
    data=[[row[0], row[1], row[2].strip(), row[3], row[4], row[5], row[6], row[7]] for row in raw_data]
    cursor.close()
    return render(request, 'graphs/addon_test_detail.html', {'data':json.dumps(data), 'set_list':set_list, 'set':set, 'start':start, 'end':end})
	
def addon_cost(request):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    mins=request.GET.get('mins', 240)
    cursor=connection.cursor()
    cursor.execute("SELECT set_code, set_exp, COUNT(*) AS COUNT, (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=t.set_code and c.Discipline!='I') as cost_per_test FROM tests t WHERE datebookedin>(SELECT MIN(datebookedin) FROM tests t1 WHERE t1.specimen_number=t.specimen_number) AND set_code not in ('PROBL', 'BHH') AND datecollected BETWEEN convert(date, %s ) AND convert(date, %s ) AND datediff(mi, datereceived, datebookedin)> %s AND consultant IN ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') GROUP BY set_code, set_exp", [start, end , mins])
    raw_data=cursor.fetchall()
    data={}
    for i in raw_data:
                t={i[0]:{'test':i[0],'test_exp':i[1],'count':i[2], 'costpertest':i[3]}}
                data.update(t)
    data2=json.dumps(data)
    cursor.close()
    return render(request, 'graphs/addon_cost.html', {'data':data2, 'start':start, 'end':end, 'mins':mins})
	
def repeats(request):
    start=request.GET.get('start', "2016-09-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    mins=request.GET.get('mins', 60)
    cursor=connection.cursor()
    cursor.execute("select set_code, set_exp, count(*), (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=q.set_code and c.Discipline!='I') as cost_per_test from(SELECT t.set_code, t.set_exp, t.patientid FROM tests t join tests t1 ON (t.patientid=t1.patientid AND t.specimen_number!=t1.specimen_number AND t.set_code=t1.set_code) WHERE t.set_code NOT IN ('SI', 'PROBL') AND datediff(mi, t.datecollected, t1.datecollected) BETWEEN 0 AND %s AND t1.datereceived BETWEEN convert(date, %s ) AND convert(date, %s ) AND (t1.consultant IN ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') and t.consultant IN ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI')) GROUP BY t.set_code, t.set_exp, t.patientid) q group by set_code, set_exp", [mins, start, end])
    raw_data=cursor.fetchall()
    data={}
    for row in raw_data:
        data[row[0]]={}
        data[row[0]]['set_exp']=row[1]
        data[row[0]]['count']=row[2]
    data2=json.dumps(data)
    sets=set([row[0] for row in raw_data])
    set_exp=set([row[0] for row in raw_data])
    set_data={}
    for i in sets:
        set_data[i]=[row[1] for row in raw_data if (row[0]==i)][0]
    cost=[row[2]*row[3] for row in raw_data]
    cost_exc_tni=[row[2]*row[3] for row in raw_data if (row[0]!='TNI')]
    cursor.close()
    return render(request, 'graphs/repeats.html', {'data':data2, 'start':start, 'end':end, 'mins':mins, 'setexp':set_exp, 'cost':cost, 'not_tni':cost_exc_tni})
	
def repeats_detail(request):
    start=request.GET.get('start', "2016-09-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    mins=request.GET.get('mins', 60)
    set=request.GET.get('set', 'UE')
    bins=request.GET.get('bins', 30)
    cursor=connection.cursor()
    cursor.execute("SELECT distinct t.set_code, t.set_exp, datediff(mi, t.datecollected, t1.datecollected), t.patientid FROM tests t join tests t1 ON (t.patientid=t1.patientid AND t.specimen_number!=t1.specimen_number AND t.set_code=t1.set_code) WHERE t.set_code = %s AND datediff(mi, t.datecollected, t1.datecollected) BETWEEN 0 and %s     AND t1.datereceived BETWEEN convert(date, %s)     AND convert(date, %s)", [set, mins, start, end])
    raw_data=cursor.fetchall()
    data=[row[2] for row in raw_data]
    if(len(data)>0):
        set_exp=[row[1] for row in raw_data][0]
    else:
        set_exp=set
    cursor.execute("select * from min_intervals where set_code=%s order by [time(hours)] asc", [set])
    raw_int=cursor.fetchall()
    int_data=[]
    for i in range(len(raw_int)):
        int_data.append([raw_int[i][0], raw_int[i][1], raw_int[i][2], raw_int[i][3]])
    cursor.execute("select distinct set_code from tests order by set_code")
    raw_set_list=cursor.fetchall()
    set_list=[row[0] for row in raw_set_list]
    return render(request, 'graphs/repeat_details.html', {'data':data,'start':start, 'end':end, 'set':set, 'mins':mins, 'int_data':int_data, 'set_list':set_list, 'bins':bins, 'set_exp':set_exp})
	
def test(request):
    return render(request, 'graphs/test.html')
	
def timeflow(request):
    start=request.GET.get('start', "2016-07-08")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    seti=request.GET.get('set', 'UE')
    cursor=connection.cursor()
    cursor.execute("select distinct set_code from tests order by set_code")
    raw_set_list=cursor.fetchall()
    set_list=[row[0] for row in raw_set_list]
    if seti=='All':
        cursor.execute("select convert(date, datereceived) as date, avg(datediff(mi, datecollected, datereceived)) as [traveltolab], avg(datediff(mi, datereceived, dateauthorised)) as [timeinlab], avg(datediff(mi, dateauthorised, dateviewed)) as [timetillview], count(*) as count from tests where datediff(mi, dateauthorised, dateviewed)>0 and datediff(mi, datereceived, dateauthorised)>0 and datereceived BETWEEN convert(date, %s) AND convert(date, %s) group by convert(date, datereceived)", [start, end])
    else:
        cursor.execute("select convert(date, datereceived) as date, avg(datediff(mi, datecollected, datereceived)) as [traveltolab], avg(datediff(mi, datereceived, dateauthorised)) as [timeinlab], avg(datediff(mi, dateauthorised, dateviewed)) as [timetillview], count(*) as count from tests where datediff(mi, dateauthorised, dateviewed)>0 and datediff(mi, datereceived, dateauthorised)>0 and set_code =%s and datereceived BETWEEN convert(date, %s) AND convert(date, %s) group by convert(date, datereceived)", [seti, start, end])
    raw_data=cursor.fetchall()
    cursor.execute("select * from outliers where set_code= %s and date BETWEEN convert(date, %s) AND convert(date, %s)", [seti, start, end])
    outliers=cursor.fetchall()
    dates=set([row[0] for row in raw_data])
    sets=set([row[1] for row in raw_data])
    data={}
    for row in raw_data:
        data[row[0]]={'travel':row[1], 'inlab':row[2], 'toview':row[3], 'count':row[4]}
        data[row[0]]['outliers']={}
        for i in ['travel', 'inlab','toview']:
            data[row[0]]['outliers'][i]=[{'specimen_number':roww[2],'time':roww[3], 'PID':roww[5]} for roww in outliers if roww[1]==row[0] and roww[4]==i]
    cursor.close()
    data2=json.dumps(data)
    return render(request, 'graphs/timeflow.html', {'data':data2, 'set_list':set_list, 'start':start, 'end':end, 'set':seti})

def compare(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    split=request.GET.get('splitby', 'ice')
    seti=request.GET.get('set', 'UE')
    cursor=connection.cursor()
    cursor.execute("select distinct set_code from tests order by set_code")
    raw_set_list=cursor.fetchall()
    set_list=[row[0] for row in raw_set_list]
    if split=='cons':
        splitby='Consultants'
        if seti=='All':
            cursor.execute("select consultantcode, left(diagnosiscode1, 1) as icd, count(*) from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) group by consultantcode, left(diagnosiscode1, 1)", [start, end])
        else:
            cursor.execute("select consultantcode, left(diagnosiscode1, 1) as icd, count(*), set_exp from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) and t.set_code=%s group by consultantcode, left(diagnosiscode1, 1), set_exp", [start, end, seti])
    elif split=='clin':
        splitby='Clinicians'
        if seti=='All':
            cursor.execute("select attendingclinician, left(diagnosiscode1, 1) as icd, count(*) from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) group by attendingclinician, left(diagnosiscode1, 1)", [start, end])
        else:
            cursor.execute("select attendingclinician, left(diagnosiscode1, 1) as icd, count(*), set_exp from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) and t.set_code=%s group by attendingclinician, left(diagnosiscode1, 1), set_exp", [start, end, seti])
    else:
        splitby='Ice Requestors'
        if seti=='All':
            cursor.execute("select specimen_taken_by, left(diagnosiscode1, 1) as icd, count(*) from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) and specimen_taken_by is not null group by specimen_taken_by, left(diagnosiscode1, 1)", [start, end])
        else:		
            cursor.execute("select specimen_taken_by, left(diagnosiscode1, 1) as icd, count(*), set_exp from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) and t.set_code=%s  and specimen_taken_by is not null group by specimen_taken_by, left(diagnosiscode1, 1), set_exp", [start, end, seti])    
    raw_data=cursor.fetchall()
    if seti=="All":
        set_exp="All Tests"
    else:
        set_exp=raw_data[0][3]
    clins=set([row[0] for row in raw_data])
    data={}
    for clin in clins:
        data[clin]={}
        data[clin]['NoDiagnosis']=0
        data[clin]['AB']=0
        data[clin]['VWXY']=0		
    for row in raw_data:
        if row[1]=="" or row[1] is None:
            data[row[0]]['NoDiagnosis']+=row[2]
        elif row[1]=='A' or row[1]=='B':
            data[row[0]]['AB']+=row[2]
        elif row[1]=='V' or row[1]=='W' or row[1]=='X' or row[1]=='Y':
            data[row[0]]['VWXY']+=row[2]
        else:
            data[row[0]][row[1]]=row[2]
    data2=json.dumps(data)
    return render(request, 'graphs/comparing_levels.html', {'set_list':set_list, 'start':start, 'end':end, 'data':data2, 'set':seti, 'splitby':splitby, 'set_exp':set_exp})	

def icd_split(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    cursor=connection.cursor()
    cursor.execute("select set_code, left(diagnosiscode1, 1) as icd, count(*) from attendance a left join tests t on t.attendanceno=a.attendanceno where episodedate between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL', 'SEND') and t.consultant in ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') group by set_code, left(diagnosiscode1, 1)", [start, end])
    raw_data=cursor.fetchall()
    set_code=set([row[0] for row in raw_data])
    data={}
    for se in set_code:
        data[se]={}
        data[se]['total']=0
        data[se]['NoDiagnosis']=0
        data[se]['AB']=0
        data[se]['VWXY']=0
    for row in raw_data:
        data[row[0]]['total']+=row[2]
        if row[1]=="" or row[1] is None:
            data[row[0]]['NoDiagnosis']+=row[2]
        elif row[1]=='A' or row[1]=='B':
            data[row[0]]['AB']+=row[2]
        elif row[1]=='V' or row[1]=='W' or row[1]=='X' or row[1]=='Y':
            data[row[0]]['VWXY']+=row[2]
        else:
            data[row[0]][row[1]]=row[2]
    data2=json.dumps(data)
    return render(request, 'graphs/icd_split.html', {'data':data2, 'start':start, 'end':end})
	
def costs_bubble(request):
    start=request.GET.get('start', "2016-07-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    view=request.GET.get('view', 'spend')
    hset=request.GET.get('highlight', 'none')
    cursor=connection.cursor()
    cursor.execute("select set_code, set_exp, count(distinct specimen_number), (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=t.set_code and c.Discipline!='I') from tests t where datereceived between convert(date, %s) and convert(date, %s) and consultant in ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') group by set_code, set_exp", [start, end])
    raw_data=cursor.fetchall()
    data={}
    sets=[(row[0],row[1]) for row in raw_data]
    for row in raw_data:
        data[row[0]]={'set_code':row[0], 'set_exp':row[1], 'count':row[2], 'cost':row[3]}
    data2=json.dumps(data)
    return render(request, 'graphs/cost_bubble.html', {'data':data2, 'test':'test', 'start':start, 'end':end, 'view':view, 'setexp':sets, 'hset':hset})
	
def costxtime(request, source):#havent made graph yet?
    start=request.GET.get('start', "2016-08-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    seti=request.GET.get('set', 'All')
    cursor=connection.cursor()
    cursor.execute("select set_code, set_exp, convert(date, datereceived), count(distinct specimen_number), (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=t.set_code and c.Discipline=t.discipline) from tests t where datereceived between convert(date, %s) and convert(date, %s) and consultant in ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') group by set_code, convert(date, datereceived), set_exp", [start, end])
    raw_data=cursor.fetchall()
    cursor.execute("select convert(date, episodedate), count(distinct patientid) from attendance where arrivaltype in ('MIN', 'MAJ', 'MWR', 'RES') and episodedate between convert(date, %s) and convert(date, %s) group by convert(date, episodedate)", [start, end])
    patient_count=cursor.fetchall()
    set_list=set([row[0] for row in raw_data])
    data={}
    for date in set([row[2] for row in raw_data]):
        data[date]={}
    for row in raw_data:
        data[row[2]][row[0]]={'set_code':row[0], 'set_exp':row[1], 'count':row[3], 'cost':row[4]}
    data2=json.dumps(data)
    pt_count={}
    for row in patient_count:
        pt_count[row[0]]=row[1]
    pt_count2=json.dumps(pt_count)
    return render(request, 'graphs/costovertime.html', {'data':data2, 'start':start, 'end':end, 'set':seti, 'set_list':set_list, 'pt_count':pt_count2})
	
def costxvisit(request):#not made yet
    cursor.execute("select convert(date, datecollected), case when attendanceno in (select attendanceno from attendance a where abs(datediff(hh, episodedate, t.datecollected))<24 and t.patientid=a.patientid) then patientID + (select min(attendanceno) from attendance a where datediff(hh, episodedate, t.datecollected)<24 and t.patientid=a.patientid) else 'fail?' end as episodeid, (select MAX(convert(float, internal_recharge)) from cost c where c.set_code=t.set_code and c.Discipline=t.discipline)as cost from tests t where datecollected between convert(date, '2016-07-24') and convert(date, '2016-09-15') order by episodeid") #not quite right as sometimes more than one date per episodeno
    raw_data=cursor.fetchall()
    return render(request, 'graphs/costovertime.html', {'data':data2})	
	
def ice_count(request):
    start=request.GET.get('start', "2016-09-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    cursor=connection.cursor()
    cursor.execute("SELECT arrivaltype, date, SUM(CASE WHEN specimen_taken_by IS NULL THEN 0 ELSE 1 END) AS ice_requested, COUNT(*) AS total FROM (SELECT DISTINCT specimen_number, arrivaltype, specimen_taken_by, convert(date, datereceived) as date FROM tests t join attendance a ON a.attendanceno=t.attendanceno WHERE datereceived BETWEEN convert(date, %s) AND convert(date, %s)) sq WHERE arrivaltype is not null AND arrivaltype != '' GROUP BY arrivaltype, date", [start, end])
    raw_data=cursor.fetchall()
    arrival=set([row[0] for row in raw_data])
    date_list=set([row[1] for row in raw_data])
    dataz={}
    for date in date_list:
        dataz[date]={}
        dataz[date]['total_count']=sum([row[3] for row in raw_data if row[1]==date])
        for arr in arrival:
            dataz[date][arr]={}
            dataz[date][arr]['ice']=sum([row[2] for row in raw_data if row[0]==arr and row[1]==date])
            dataz[date][arr]['count']=sum([row[3] for row in raw_data if row[0]==arr and row[1]==date])		
    data2=json.dumps(dataz)			
    return render(request, 'graphs/ice_count_by_area.html', {'start':start, 'end':end, 'data':data2})
	
def not_ice_count(request):
    start=request.GET.get('start', "2016-09-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    cursor=connection.cursor()
    cursor.execute("SELECT arrivaltype, date, SUM(CASE WHEN specimen_taken_by IS NULL THEN 0 ELSE 1 END) AS ice_requested, COUNT(*) AS total FROM (SELECT DISTINCT specimen_number, arrivaltype, specimen_taken_by, convert(date, datereceived) as date FROM tests t join attendance a ON a.attendanceno=t.attendanceno WHERE datereceived BETWEEN convert(date, %s) AND convert(date, %s)) sq WHERE arrivaltype is not null AND arrivaltype != '' GROUP BY arrivaltype, date", [start, end])
    raw_data=cursor.fetchall()
    arrival=set([row[0] for row in raw_data])
    date_list=set([row[1] for row in raw_data])
    dataz={}
    for date in date_list:
        dataz[date]={}
        dataz[date]['total_count']=sum([row[3] for row in raw_data if row[1]==date])
        for arr in arrival:
            dataz[date][arr]={}
            dataz[date][arr]['ice']=sum([row[2] for row in raw_data if row[0]==arr and row[1]==date])
            dataz[date][arr]['count']=sum([row[3] for row in raw_data if row[0]==arr and row[1]==date])		
    data2=json.dumps(dataz)			
    return render(request, 'graphs/not_ice_count.html', {'start':start, 'end':end, 'data':data2})	

def ice(request):
    start=request.GET.get('start', "2016-09-01")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    cursor=connection.cursor()
    cursor.execute("select convert(date, datereceived) AS date, count(*) as total, SUM(CASE WHEN specimen_taken_by IS NULL THEN 0 ELSE 1 END) AS ice_requested from tests WHERE datereceived BETWEEN convert(date, %s) AND convert(date, %s) AND consultant IN ('AECONS','ASI','BARO','BOD','ERI','GUP','ISM','JONE','LAI','MACAID','MIST','NAR','OCA','PAR','RAGU','RAHS','RAVE','ROSE','SAJ','VIJ','WRI') group by convert(date, datereceived)", [start, end])
    raw_data=cursor.fetchall()
    data={}
    for row in raw_data:
        data[row[0]]={'ice':row[2], 'total':row[1]}
    data2=json.dumps(data)	
    return render(request, 'graphs/ice.html', {'start':start, 'end':end, 'data':data2})
	
def bundles(request):
    return render(request, 'graphs/bundles.html')
	
def requesting_levels(request, source):
    start=request.GET.get('start', "2016-07-15")
    end=request.GET.get('end', time.strftime("%Y-%m-%d"))
    username=None
    if request.user.is_authenticated():
        username = request.user.username
    cursor=connection.cursor()
    if source=='ice':
        clin=request.GET.get('clin', 'BelRob')
        cursor.execute("select distinct specimen_taken_by from tests where specimen_taken_by is not null order by specimen_taken_by asc")
        clinician_list=[row[0] for row in cursor.fetchall()]
        if clin=="All":
            cursor.execute("select set_code, set_exp, count(*) from tests where datecollected between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL') group by set_code, set_exp order by count(*) desc", [start, end])
        else:
            cursor.execute("select set_code, set_exp, count(*) from tests where specimen_taken_by=%s and datecollected between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL') group by set_code, set_exp order by count(*) desc", [clin, start, end])
        raw_data=cursor.fetchall()
    elif source=='con':
        cursor.execute("select distinct consultant from tests order by consultant")
        clinician_list=[row[0] for row in cursor.fetchall()]
        clin=request.GET.get('clin', 'AECONS')
        if clin=="All":
            cursor.execute("select set_code, set_exp, count(*) from tests where datecollected between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL') group by set_code, set_exp order by count(*) desc", [start, end])
        else:
            cursor.execute("select set_code, set_exp, count(*) from tests where datecollected between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL') and consultant=%s group by set_code, set_exp order by count(*) desc", [start, end, clin])   
        raw_data=cursor.fetchall()		
    elif source=='clin':	
        cursor.execute("select distinct attendingclinician from attendance where attendingclinician is not null and attendingclinician !='' order by attendingclinician")
        clinician_list=[row[0] for row in cursor.fetchall()]
        clin=request.GET.get('clin', 'ORBT')
        if clin=="All":
            cursor.execute("select t.set_code, set_exp, count(*) from tests t join attendance a on t.attendanceno=a.attendanceno where datediff(mi, episodedate, datecollected)<timeinae and datecollected between convert(date, %s) and convert(date, %s) and set_code not in ('SI', 'PROBL') group by t.set_code, set_exp order by count(*) desc", [start, end]) 
        else:
            cursor.execute("select t.set_code, set_exp, count(*) from tests t join attendance a on t.attendanceno=a.attendanceno where datediff(mi, episodedate, datecollected)<timeinae and datecollected between convert(date, %s) and convert(date, %s) and attendingclinician=%s and set_code not in ('SI', 'PROBL') group by t.set_code, set_exp order by count(*) desc", [start, end, clin])   
        raw_data=cursor.fetchall()	
    data=[]
    for row in raw_data:
        data.append([row[0], row[1], row[2]])
	data2=json.dumps(data)
    return render(request, 'graphs/Requesting_levels.html', {'clinician_list':clinician_list, 'start':start, 'end':end, 'clin':clin, 'data':data2, 'source':source})	
	
	
	