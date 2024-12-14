from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Category

def post_list(request):
    """
    View para listar os posts com suporte a busca, filtro por categoria e paginação.
    """
    # Obtém parâmetros de busca e filtro da URL
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    
    # Inicializa a lista de posts
    posts_list = Post.objects.all().order_by('-created_at')

    # Filtra por busca se 'q' estiver presente
    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Filtra por categoria se 'category' estiver presente
    if category_filter:
        posts_list = posts_list.filter(category__name__iexact=category_filter)

    # Configura a paginação (6 posts por página)
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtém todas as categorias para o filtro
    categories = Category.objects.all()
    
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category_filter': category_filter,
        'categories': categories
    })

def post_detail(request, pk):
    """
    View para exibir os detalhes de um post específico, incluindo comentários aprovados.
    """
    # Obtém o post ou retorna 404 se não existir
    post_obj = get_object_or_404(Post, pk=pk)
    # Obtém comentários aprovados relacionados ao post
    comments = post_obj.comments.filter(approved=True).order_by('-created')

    # Processa o formulário de comentário
    if request.method == "POST":
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=post_obj, name=name, body=body)
            return redirect('post_detail', pk=post_obj.pk)

    return render(request, 'blog/post_detail.html', {
        'post': post_obj,
        'comments': comments,
    })

def user_login(request):
    """
    View para lidar com o login de usuários.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
    return render(request, 'blog/login.html')

def user_logout(request):
    """
    View para lidar com o logout de usuários.
    """
    logout(request)
    return render(request, 'blog/logout.html')

def register(request):
    """
    View para lidar com o registro de novos usuários.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('post_list')
    return render(request, 'blog/register.html')

def sobre(request):
    """
    View simples que renderiza a página "Sobre".
    """
    return render(request, 'blog/sobre.html', {})
