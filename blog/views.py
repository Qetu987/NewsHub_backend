from django.shortcuts import render, redirect
from django.views.generic.base import View
from blog.models import Post, Like, Reviews
from django.contrib.auth.models import AnonymousUser


class Posts_list_base(View):
    anonimys = AnonymousUser()

    def get_post_data(self, queryset):
        data = list()
        for post in queryset:
            likes = Like.objects.filter(post=post)
            comments = Reviews.objects.filter(post=post)
            post_data = {
                # модифицируем если надо что-то добавить в инфо про пост
                'post_data': post,
                'likes': likes,
                'comments': comments,
            }
            data.append(post_data)
        return data
    
    def get(self, request):
        context = self.get_data()
        return render(request, self.template_name, context)


class PostsList(Posts_list_base):
    template_name = "blog/post_list.html"
    
    def get_data(self):
        queryset = Post.objects.filter(draft=False).order_by('-date')
        data = self.get_post_data(queryset)

        # окнтекст страницы
        context = {
            'posts_list': data,
        }

        return context
