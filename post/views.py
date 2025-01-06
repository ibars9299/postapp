from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from requests import Response
from post.forms import LoginForm, PostForm, RegisterForm
from post.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from django.contrib.auth.models import User

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            return redirect('home')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')  # En yeni postlar üstte
    context = {
        'form': form, 
        'posts': posts,
        'user': request.user  # Kullanıcı bilgisini ekledik
    }
    return render(request, 'post/home.html', context)

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)  # Gönderiyi al.
    post.delete()  # Gönderiyi sil.
    return redirect('home')  # İşlem tamamlanınca ana sayfaya yönlendirin.

@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)  # Gönderiyi al.
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Formu eski gönderi ile bağla.
        if form.is_valid():  # Formun doğruluğunu kontrol et.
            form.save()  # Veritabanına kaydet.
            return redirect('home')  # İşlem tamamlanınca ana sayfaya yönlendir.
    else:
        form = PostForm(instance=post)  # GET isteği için formu eski gönderi ile doldur.

    return render(request, 'post/update.html', {'form': form})  # Şablona formu gönder.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Formdan alınan verilerle kullanıcıyı doğrula
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Kullanıcıyı giriş yaptır
                return redirect('home')  # Başka bir sayfaya yönlendir
            else:
                form.add_error(None, 'Geçersiz kullanıcı adı veya şifre')  # Hata mesajı
    else:
        form = LoginForm()

    return render(request, 'post/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            
            # Şifrelerin uyuşup uyuşmadığını kontrol et
            if password != password2:
                form.add_error('password2', 'Şifreler uyuşmuyor')  # 'password2' alanına hata ekle
            else:
                # Kullanıcıyı oluştur
                if User.objects.filter(username=username).exists():
                    form.add_error('username', 'Bu kullanıcı adı zaten alınmış.')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)  # Otomatik olarak giriş yap
                    return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'post/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
@api_view(['GET'])
def data_view(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        user = User.objects.get(id=post.user_id)
        data.append({
            'post': {
                'title': post.title,
                'image': post.image.url if post.image else None,  # Eğer resim yoksa bir URL dönmesi için boş string at.
                'content': post.content,
                'created_at': post.created_at,
            },
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })
    return Response(data)
    