from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Post, Comment

def post_list(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post_obj = get_object_or_404(Post, pk=pk)
    comments = post_obj.comments.filter(approved=True).order_by('-created')

    if request.method == "POST":
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=post_obj, name=name, body=body)
            return redirect('post_detail', pk=post_obj.pk)

    return render(request, 'blog/post_detail.html', {'post': post_obj, 'comments': comments})

def search_posts(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'blog/search_results.html', {'query': query, 'results': results})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    return render(request, 'blog/logout.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # Usuário já existe - aqui seria bom mostrar uma mensagem, mas vamos apenas ignorar por enquanto.
                pass
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('post_list')
    return render(request, 'blog/register.html')
