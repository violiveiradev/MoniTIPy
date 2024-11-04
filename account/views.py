from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Substitua 'home' pela página de destino pós-login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# View para listar usuários
def user_list(request):
    users = User.objects.all()
    return render(request, 'account/user-management.html', {'users': users})

# View para adicionar usuário
def add_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        group_name = request.POST.get('group')

        # Verifica se as senhas coincidem
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('add_user')

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return redirect('add_user')

        # Cria o novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name  # Salva o nome completo no campo first_name
        user.save()

        # Adiciona o usuário ao grupo, se especificado
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        messages.success(request, 'Usuário adicionado com sucesso!')
        return redirect('user_list')

    # Obtém todos os grupos para exibir no formulário
    groups = Group.objects.all()
    return render(request, 'account/add-user.html', {'groups': groups})


# View para editar usuário
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        group_name = request.POST.get('group')

        # Verifica se as senhas coincidem, caso uma nova senha seja informada
        if password and password == confirm_password:
            user.set_password(password)
        elif password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('edit_user', user_id=user.id)

        user.first_name = full_name  # Salva o nome completo
        user.save()

        # Atualiza o grupo do usuário
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.set([group])

        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('user_list')

    groups = Group.objects.all()  # Para exibir no formulário
    return render(request, 'account/edit-user.html', {'user': user, 'groups': groups})

# View para excluir usuário
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Usuário excluído com sucesso!')
    return redirect('user_list')