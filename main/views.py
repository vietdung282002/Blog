from django.contrib.auth import logout
from .models import Post, User, Comment
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView
from .forms import *


# Create your views here.

def home(request):
    feature_post = Post.objects.all().order_by('-id')
    param = {'feature_post': feature_post}
    return render(request, 'home.html', param)


def logout_view(request):
    logout(request)
    return redirect('/')


def search(request):
    print("121312")
    query = request.GET.get('query')
    search_user = NewUser.objects.filter(username=query)
    search_user_posts = Post.objects.filter(user__username__icontains=query)
    search_title = Post.objects.filter(title__icontains=query)
    search_content = Post.objects.filter(content__icontains=query)
    search_result = search_title.union(search_content, search_user_posts)

    param = {'search_result': search_result,
             'search_term': query, 'search_user': search_user}
    return render(request, 'search.html', param)


def view_profile(request, user_name):
    try:
        user_obj = NewUser.objects.get(username=user_name)
        print(user_obj.username)
    except ObjectDoesNotExist:
        return HttpResponse('User does not exists.')

    user_posts = user_obj.post_set.all().order_by('-id')

    param = {'user_posts': user_posts, 'user_data': user_obj}
    print(param.get('user_data').profile_pic.url)

    try:
        return render(request, 'profile.html', param)
    except:
        messages.warning(
            request, f"You have to login before access {user_name}'s profile.")
        return redirect('home')


def view_post(request, post_title):
    get_post = Post.objects.get(title=post_title)
    # all_rel_posts = Post.objects.filter(user__username=get_post.user)
    all_rel_posts = Post.objects.filter(
        user__username=get_post.user).exclude(title=post_title)
    post_comments = get_post.comment_set.all().order_by('-id')
    param = {'post_data': get_post, 'all_posts': all_rel_posts,
             'post_comments': post_comments}
    return render(request, 'post.html', param)


def add_comment(request, post_title, user_name):
    name = user_name
    comment = request.POST.get('comment')
    post = Post.objects.get(title=post_title)
    if name != "" and comment != "":
        create_comment = Comment(post=post, name=name, comment=comment)
        create_comment.save()
        return HttpResponseRedirect(reverse('view_post', args=[str(post_title)]))


def delete_post(request, post_title):
    get_post = Post.objects.get(title=post_title)
    get_post.delete()
    messages.success(request, 'Post has been deleted succsfully.')
    return redirect(f'/profile/{get_post.user.username}')


def delete_comment(request, post_title, comment_id):
    get_post = Comment.objects.get(id=comment_id)
    get_post.delete()
    messages.success(request, 'Comment has been deleted succsfully.')
    return redirect(f'/post/{post_title}')


class WritePostView(ListView):
    model = Post
    template_name = 'main/create_post.html'

    def get(self, request, user_name):
        form = WritePostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_name):
        form = WritePostForm(request.POST)
        if form.is_valid():
            count = 0
            feature_post = Post.objects.all().order_by('-id')[:3]
            user_obj = NewUser.objects.get(username=user_name)
            title = form.cleaned_data['title']
            for post in feature_post:
                if title == post.title:
                    count += 1

            if count > 0:
                title = title + " (" + str(count) + ")"

            content = form.cleaned_data['content']
            add_post = self.model.objects.create(
                user=user_obj, title=title, content=content)
            add_post.save()

            messages.success(request, 'Post has been uploaded succsfully.')
            return redirect('/profile/' + user_name)
