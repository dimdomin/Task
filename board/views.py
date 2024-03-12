from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest, request
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView

from Task.settings import DEFAULT_FROM_EMAIL
from .forms import PostForm
from .models import Post, Response


class PostList(ListView):  # список объявлений
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = '-data_creation'
    paginate_by = 10  # вывод 10 записей на страницу


class PostListProfile(ListView):  # список объявлений
    model = Post
    template_name = 'profile/posts_profile.html'
    context_object_name = 'posts_profile'
    ordering = '-data_creation'
    paginate_by = 10  # вывод 10 записей на страницу

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDetail(DetailView):  # детали объявления
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        responses = Response.objects.filter(post=post)
        context['responses'] = responses
        return context


@login_required
def profile(request):       # профиль
    # Получаем объявления пользователя
    posts = Post.objects.filter(author=request.user)

    # Получаем все отклики на объявления пользователя
    responses = Response.objects.filter(post__in=posts)

    # Получаем выбранное объявление для фильтрации
    selected_post_id = request.GET.get('post_id')
    if selected_post_id:
        responses = responses.filter(post_id=selected_post_id)

    return render(request, 'profile/profile_response.html', {'posts': posts, 'responses': responses})


def add_post(request):  # создать объявление
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.request = request
            post_item.save()
            return redirect('posts_profile')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


def edit_post(request, post_id=None):  # редактировать объявление
    item = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('posts_profile')
    return render(request, 'posts/post_form.html', {'form': form})


def delete_post(request, post_id):  # удалить объявление
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('posts_profile')

    return render(request, 'posts/post_delete.html', {'post': post})


@login_required
def create_response(request, post_id):          # создание отклика
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        response = Response(author=request.user, post=post, content=content)
        response.save()

        # отправляем уведомление
        subject = 'Новый отклик на объявление'
        message = f'Новый отклик на ваше объявление: {post.title}'
        from_email = DEFAULT_FROM_EMAIL
        to_email = post.author.email
        send_mail(subject, message, from_email, [to_email])

        return HttpResponseRedirect('/posts/{}'.format(post_id))

    return render(request, 'create_response.html', {'post': post})


@login_required
def response_status(request, response_id, action):      # принять или отклонить отклик
    response = get_object_or_404(Response, id=response_id)
    if action == 'accept':
        response.status = 'accepted'
        subject = 'Ваш отклик принят'
        message = f'Ваш отклик на объявление "{response.post.title}" принят'
    elif action == 'reject':
        response.status = 'rejected'
        subject = 'Ваш отклик отклонен'
        message = f'Ваш отклик на объявление "{response.post.title}" отклонен'
    else:
        # Обработка неверного действия
        return HttpResponseBadRequest('Неверное действие')

    response.save()

    # отправляем уведомление на почту
    from_email = DEFAULT_FROM_EMAIL
    to_email = response.author.email
    send_mail(subject, message, from_email, [to_email])

    return redirect('post', post_id=response.post.id)
