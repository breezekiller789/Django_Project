#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


# home page變成從這邊load
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# 讓使用者可以看到特定的文章
class PostDetailView(DetailView):
    model = Post


# 讓使用者新增po文
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # 讓django知道這則新貼文的作者就是這個請求的使用者
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# 讓使用者更新自己的貼文，為了避免其他人更改別人的貼文，所以要傳入
# LoginRequiredMixin, UserPassesTestMixin這兩個參數，不然大家都可以更新別人文章
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # 當使用者成功update之後，django會不知道要帶使用者回去哪邊，所以這個要在models.py裡面定義
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # 這邊就是在避免他人刪除他人的文章，所以要檢查文章作者跟請求的使用者有無一樣
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# 讓使用者刪除文章，一樣要檢查權限，所以傳入兩個參數。
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'   # 當使用者成功刪除之後，帶他回主頁面

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
