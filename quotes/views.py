from django.shortcuts import render , redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
##    pk_3021916cc260453c8df94cf453927e5f
    import requests
    import json

    if request.method == "POST" :
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_3021916cc260453c8df94cf453927e5f")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request,'quotes/home.html',{'api': api})
    else:        
        return render(request,'quotes/home.html',{'ticker': "Please enter a ticker symbol above.."})

   
def about(request):
    return render(request, 'quotes/about.html',{})


def add_stock(request):
    import requests
    import json
    
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect("add_stock")
    else:
        ticker = Stock.objects.all()
        api_list = []
        for item in ticker:            
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(item) + "/quote?token=pk_3021916cc260453c8df94cf453927e5f")
            try:
                api = json.loads(api_request.content)                
            except Exception as e:
                api = "Error..."
            api_list.append(api)
        
        return render(request, 'quotes/add_stock.html',{'api_list':api_list})


def delete_stock(request, stock_id):
    item = Stock.objects.get(pk = stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect("delete")

def delete(request):
    ticker = Stock.objects.all()
    return render(request, 'quotes/delete_stock.html',{'ticker':ticker})
        
