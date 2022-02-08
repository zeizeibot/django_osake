from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_365dd7a8defe45258a66ccc6a65d488b")
		
		try:
			api = json.loads(api_request.content)
			
		except Exception as e:
			api = "Error..."

		#api['ytdChange'] = int(api['ytdChange'])
		api['ytdChange'] = api['ytdChange'] * 1000	
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Kirjoita etsimäsi osakekurssi tuohon ylös"})
	

	

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json
	import math

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Osake on lisätty!"))
			return redirect('add_stock')
			
	else:
		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_365dd7a8defe45258a66ccc6a65d488b")

			try:

				api = json.loads(api_request.content)
				#api['ytdChange'] = math.trunc(api['ytdChange'])
				api['ytdChange'] = api['ytdChange'] * 1000
				api.update({'tickerid':ticker_item.id})
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Osake on poistettu!"))
	return redirect(add_stock)


	#api.ytdChange = int(api.ytdChange)
	#		api.ytdChange = api.ytdChange * 100