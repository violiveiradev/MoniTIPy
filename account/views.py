from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

#@login_required
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# View para listar usuários
@login_required
def user_list(request):
    # Obter o valor de busca, se existir
    search_query = request.GET.get('search', '')

    # Filtrar usuários com base no nome completo ou nome de usuário
    if search_query:
        users = (User.objects.filter(username__icontains=search_query) | 
                 User.objects.filter(first_name__icontains=search_query) | 
                 User.objects.filter(last_name__icontains=search_query) |
                 User.objects.filter(email__icontains=search_query))
    else:
        users = User.objects.all()

    # Pré-carregar os grupos para cada usuário
    users = users.prefetch_related('groups')

    # Configuração da paginação
    paginator = Paginator(users, 1)  # 10 usuários por página
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    return render(request, 'account/user-management.html', {'users': users_page, 'search_query': search_query})


# View para adicionar usuário
@login_required
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
@login_required
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
@login_required
def delete_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('selected_users')
        User.objects.filter(id__in=user_ids).delete()
        messages.success(request, 'Usuários selecionados excluídos com sucesso.')
    return redirect('user_list')


@login_required
def edit_profile(request):
    user = request.user

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
            return redirect('edit_profile')

        user.first_name = full_name  # Salva o nome completo
        user.save()

                # Atualiza o grupo do usuário
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.set([group])

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('edit_profile')
    
    groups = Group.objects.all()
    return render(request, 'account/edit-profile.html', {'user': user, 'groups': groups})