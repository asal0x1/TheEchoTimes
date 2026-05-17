from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import F, Max, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tornado.httputil import qs_to_qsl

from .forms import CommentsForm
from .models import *


# Create your views here.


def home(request):
    news = News.objects.all()
    last_new = News.objects.order_by('-id').first()
    last_news = News.objects.order_by('-id')

    fashions = News.objects.filter(category__name='Fashion').order_by('-id')
    foods = News.objects.filter(category__name='Food').order_by('-id')
    gaming = News.objects.filter(category__name='Gaming').order_by('-id')

    most_seen = news.order_by('-views')

    ctx = {'news': news,
    'last_news': last_news,
    'last_new': last_new,
    'most_seen': most_seen,
    'fashions': fashions,
    'foods': foods,
    'gaming': gaming,
    }
    return render(request, 'index.html', ctx)

def about(request, pk):
    news = News.objects.all()

    category = Category.objects.all()
    most_seen = news.order_by('-views')

    about_post = get_object_or_404(News, pk=pk)
    comments = about_post.comments.filter(is_approved=True)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = about_post
            comment.author = request.user
            comment.save()
            return redirect('about', pk=about_post.pk)
    else:
        form = CommentsForm()

    News.objects.filter(pk=pk).update(views = F('views') + 1)
    about_post.refresh_from_db()

    ctx = { 'post': about_post,
            'comments': comments,
            'form': form,
            'category': category,
            'most_seen': most_seen,
    }
    return render(request, 'post-details.html', ctx)

def category(request, slug):
    category = Category.objects.get(slug = slug)
    news = News.objects.filter(category=category)

    ctx = {
        'news': news,
        'category': category,
    }

    return render(request, 'category.html', ctx)

def category_view(request):
    category = Category.objects.all()
    ctx = {
        'category': category,
    }
    return render(request, 'category.html', ctx)


def technology(request):
    techs = News.objects.filter(category__name='Texnologiya').order_by('-id')
    last_tech = techs.order_by('-id').first()
    most_seen = techs.order_by('-views')
    tech_tags = Category.objects.filter(news__category__name='Texnologiya').distinct()

    ctx = {
        'techs': techs,
        'last_tech': last_tech,
        'most_seen': most_seen,
        'tech_tags': tech_tags,
    }

    return render(request, 'technology.html', ctx)

def fashion(request):
    fashions = News.objects.filter(category__name='Fashion').order_by('-id')
    last_f = fashions.order_by('-id').first()
    most_seen = fashions.order_by('-views')
    f_tags = Category.objects.filter(news__category__name='Fashion').distinct()

    ctx = {
        'fashions': fashions,
        'last_f': last_f,
        'most_seen': most_seen,
        'f_tags': f_tags,
    }

    return render(request, 'fashion.html', ctx)

def sports(request):
    sports = News.objects.filter(category__name='Sport').order_by('-id')
    last_sport = sports.order_by('-id').first()
    most_seen = sports.order_by('-views')
    s_tags = Category.objects.filter(news__category__name='Sport').distinct()

    ctx = {
        'sports': sports,
        'last_sport': last_sport,
        'most_seen': most_seen,
        's_tags': s_tags
    }

    return render(request, 'sports.html', ctx)

def foods(request):
    foods = News.objects.filter(category__name='Food').order_by('-id')
    last_foods = foods.order_by('-id').first()
    most_seen = foods.order_by('-views')
    f_tags = Category.objects.filter(news__category__name='Food').distinct()

    ctx = {
        'foods': foods,
        'last_foods': last_foods,
        'most_seen': most_seen,
        's_tags': f_tags
    }

    return render(request, 'food.html', ctx)

def gaming(request):
    gaming = News.objects.filter(category__name='Gaming').order_by('-id')

    last_gaming = gaming.order_by('-id').first()
    comments = last_gaming.comments.filter(is_approved=True)

    most_seen = gaming.order_by('-views')
    g_tags = News.objects.filter(tags__name='Game Guides').distinct()



    ctx = {
        'gaming': gaming,
        'last_gaming': last_gaming,
        'most_seen': most_seen,
        'g_tags': g_tags,
        'comments': comments
    }
    return render(request, 'gaming.html', ctx)

def politics(request):
    politics = News.objects.filter(category__name='Siyosat').order_by('-id')
    last_politic = politics.order_by('-id').first()
    most_seen = politics.order_by('-views')
    p_tags = Category.objects.filter(news__category__name='Siyosat').distinct()

    ctx = {
        'politics': politics,
        'last_politic': last_politic,
        'most_seen': most_seen,
        'p_tags': p_tags
    }

    return render(request, 'politics.html', ctx)

def search(request):
    q = request.GET.get('q')
    news = News.objects.all()
    category = Category.objects.all()

    if q:
        news = news.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)|
        Q(author_name__icontains=q)
        )
    ctx = {
        'q': q,
        'category': category,
        'news': news,
    }

    return render(request, 'search.html', ctx)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username' or '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Username yoki parol xato!')
            return redirect('login')
        login(request, user)
        messages.success(request, "Kirdingiz!")
        return redirect('home')


    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username' or '').strip()
        email = request.POST.get('email' or '').strip()
        password1 = request.POST.get('password1' or '').strip()
        password2 = request.POST.get('password2' or '').strip()

        if not username or not password1:
            messages.error(request, 'Username yoki parol kiritilmagan! ')

        if password1 != password2:
            messages.error(request, "Parollar mos kelmayapti! ")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bunday email allaqachon bor! ")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)

        user.save()
        messages.success(request, "Ro'yhatdan o'tdingiz !")

        return redirect('login')

    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect("login")
