from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    log.debug('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip,
    ))
@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')
    log.debug('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))

def like(request,pk):  #좋아요
    article = get_object_or_404(Article,pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        return redirect('boards:detail',article.pk)
    else:
        article.like_users.add(request.user)
        return redirect('boards:detail',article.pk)

# Create your views here.
def index(request):
    articles = Article.objects.all()
    articles = articles.order_by('-created_at')
    page = request.GET.get('page')
    paginator = Paginator(articles,10)
    # paginator = Paginator(content_list,10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page =1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    #정렬기능
    # sort = request.GET.get('sort','')
    # if sort =='likes':
    #     content_list = Content.objects.all().order_by('-like_count','-date')
    # elif sort == 'comments':
    #     content_list = Content.objects.all().order_by('-comment_count','-date')
    # else:
    #     content_list = Content.objects.all().order_by('-date')

    # page = request.GET.get('page','')
    # posts = paginator.get_page(page)
    # board = Board.objects.all()
    
    context = {
        'articles' : articles,
        'page_obj': page_obj,
        'paginator' : paginator,
        
        
    }
    return render(request,'boards/index.html',context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comment_view=Comment.objects.filter(article=pk)
    context = {
        'article': article,
        'comment_form':comment_form,
        'comment_view':comment_view,
    }
    
    article.reads += 1
    article.save()
    return render(request, 'boards/detail.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('boards:detail', article.pk)
    else:
        form = ArticleForm()
    context = {'form': form,}
    return render(request, 'boards/create.html', context)

@require_POST
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('boards:index')

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('boards:detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form, 'article': article}
    return render(request, 'boards/update.html', context)

@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect('boards:detail', article.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('boards:detail', article_pk)