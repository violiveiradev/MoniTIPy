from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'home/home.html')


def settings(request):
    if request.method == 'POST':
        # Processar a atualização do usuário aqui
        pass
    return render(request, 'home/settings.html')