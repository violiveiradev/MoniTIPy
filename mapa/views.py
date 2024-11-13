from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def mapa_view(request):
    return render(request, 'mapa/mapa.html')
