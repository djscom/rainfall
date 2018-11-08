from django.shortcuts import render
from .models import Weather
from django.forms.models import model_to_dict
import datetime
from datetime import timedelta

def index(request):
    latest_rain = Weather.objects.exclude(rain_trace='-').exclude(rain_trace='0.0').order_by('-local_date_time_full').values()
    first_data_point = model_to_dict(Weather.objects.order_by('local_date_time_full').first())
	
    temp = latest_rain[0]
    rainfall = []
    i = 0
	
    for lr in latest_rain:		
        dt = datetime.datetime.strptime(lr['local_date_time_full'][:12], "%Y%m%d%H%M")
        lr['local_date_time_full'] = dt
        if i == 0:
            rainfall.append(lr)
        else:
            if dt < datetime.datetime.combine(rainfall[-1]['local_date_time_full'].date() - timedelta(days=1), datetime.time(9,0)):
                rainfall.append(lr)
        i += 1
	
    first_datapoint = datetime.datetime.strptime(first_data_point['local_date_time_full'][:8], "%Y%m%d")
    first_datapoint = first_datapoint.strftime("%Y.%m.%d")

    record_count = Weather.objects.count()
	
    context = {'rainfall': rainfall,'firstdatapoint': first_datapoint,'recordcount': record_count}
    return render(request, 'rain/index.html', context)
