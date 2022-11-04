from django.shortcuts import render
from django.http import request
from .utils.gameRecommender import gameRecommender
# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            context={}
            favgame = request.POST.get("fav_game")
            grecomm = gameRecommender()
            context["recommendedGames"] = grecomm.getRecommendedGames(favgame)
            return render(request,"main/results.html",context=context)
        except Exception as err:
            print(err)
            return render(request,"main/error.html",context={"err":err})
    return render(request, "main/home.html")

def about(request):
    return render(request,"main/about.html")