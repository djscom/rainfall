from django.core.management import BaseCommand
from rain.models import Weather
import requests, json

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	# Show this when the user types help
	help = "My test command"

	# A command must define handle()
	def handle(self, *args, **options):
		self.stdout.write("Getting weather data from the Australian Bureau of Meteorology")
		url = "http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95551.json"
		data = requests.get(url).json()
		
		count = 0
		for rain in data['observations']['data']:
			if (not Weather.objects.filter(aifstime_utc=rain['aifstime_utc']).exists()) and (rain['rain_trace'] != '-' or rain['rain_trace'] != '0.0'):
				count = count + 1
				r = Weather(swell_period=rain['swell_period'], \
				 wind_dir=rain['wind_dir'],lat = rain['lat'], \
				 cloud_oktas=rain['cloud_oktas'],gust_kt=rain['gust_kt'], \
				 history_product = rain['history_product'], \
				 local_date_time_full = rain['local_date_time_full'], \
				 cloud = rain['cloud'],press_msl = rain['press_msl'], \
				 cloud_type = rain['cloud_type'], \
				 wind_spd_kmh = rain['wind_spd_kmh'], \
				 lon = rain['lon'],swell_height = rain['swell_height'], \
				 wmo = rain['wmo'],press_qnh = rain['press_qnh'], \
				 weather = rain['weather'],wind_spd_kt = rain['wind_spd_kt'], \
				 rain_trace = rain['rain_trace'],aifstime_utc = rain['aifstime_utc'], \
				 delta_t = rain['delta_t'],press_tend = rain['press_tend'], \
				 rel_hum = rain['rel_hum'],local_date_time = rain['local_date_time'], \
				 press = rain['press'],vis_km = rain['vis_km'], \
				 sea_state = rain['sea_state'],air_temp = rain['air_temp'], \
				 name = rain['name'],cloud_base_m = rain['cloud_base_m'], \
				 cloud_type_id = rain['cloud_type_id'],gust_kmh = rain['gust_kmh'], \
				 dewpt = rain['dewpt'],swell_dir_worded = rain['swell_dir_worded'], \
				 sort_order = rain['sort_order'],apparent_t = rain['apparent_t'])
				r.save()
		self.stdout.write(str(count) + " records added")
