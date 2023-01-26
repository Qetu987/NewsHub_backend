from django.shortcuts import render, redirect
from django.views.generic.base import View
from blog.models import Post, Like, Reviews
from django.contrib.auth.models import AnonymousUser
from blog.forms import LikeForm


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
                'user_likes': [i['user'] for i in Like.objects.values('user').filter(post=post)],
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

class LikePost(View):
    anonimys = AnonymousUser()

    def post(self, request):
        form = LikeForm(request.POST)
        if form.is_valid() and request.user != self.anonimys:
            post = form.cleaned_data.get('post')
            likes = Like.objects.filter(post=post)
            if request.user in [like.user for like in likes]:
                obj = Like.objects.get(post=form.cleaned_data.get('post'), user=request.user)
                obj.delete()
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
        return redirect('home')
