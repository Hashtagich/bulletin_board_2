from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView

from fmmo.settings import EMAIL_HOST_USER, SITE_URL
from .filters import ResponseFilter, MyResponseFilter
from .forms import PostForm, ResponseForm
from .mixins import AuthorRequiredMixin, AuthorNecessaryMixin
from .models import Post, User, Response
from django.db.models import Q


# Create your views here.
class HomeView(TemplateView):
    template_name = 'flatpages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostsListView(ListView):
    model = Post
    ordering = '-datetime_post'
    template_name = 'fan_forum/posts.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'fan_forum/post.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'fan_forum/post_create.html'
    context_object_name = 'post'

    permission_required = (
        'fan_forum.view_post',
        'fan_forum.add_post',
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.save()
            return redirect('/')
        else:
            form = PostForm()
        return render(request, 'fan_forum/post_create.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    model_search = Post
    template_name = 'fan_forum/post_edit.html'
    form_class = PostForm
    permission_required = (
        'fan_forum.view_post',
        'fan_forum.change_post',
    )

    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Post.objects.get(pk=my_id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    model_search = Post
    template_name = 'fan_forum/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = (
        'fan_forum.view_post',
        'fan_forum.delete_post',
    )


class PersonalAccountView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/personal_account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']  # Получаем значение идентификатора пользователя из URL
        context['user'] = User.objects.get(id=user_id)  # Получаем конкретного пользователя по его ID
        return context


class ResponseCreateView(LoginRequiredMixin, AuthorNecessaryMixin, CreateView):
    model = Response
    model_search = Post
    form_class = ResponseForm
    template_name = 'fan_forum/response_create.html'
    context_object_name = 'response'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')  # Получаем идентификатор post из URL
        post = get_object_or_404(Post, pk=post_id)  # Получаем объект Post по идентификатору

        response = form.save(commit=False)
        response.post = post
        response.author = self.request.user.author
        response.save()

        # Отправка электронного сообщения
        recipient_email = post.author.user.email
        html_context = render_to_string(
            'email/notification_new_response.html',
            {
                'text': response.text,
                'link': f'{SITE_URL}/response/{response.pk}',
                'title': post.title,
                'author': response.author.user.username,
                'preview': response.preview(),
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Новый отклик на ваш пост',
            body='',
            from_email=EMAIL_HOST_USER,
            to=[recipient_email],
        )
        msg.attach_alternative(html_context, 'text/html')
        msg.send()

        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'fan_forum/response.html'
    context_object_name = 'response'


class ResponseUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Response
    model_search = Response
    template_name = 'fan_forum/response_edit.html'
    form_class = ResponseForm

    permission_required = (
        'fan_forum.view_response',
        'fan_forum.change_response',
    )

    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Response.objects.get(pk=my_id)


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fan_forum/response_delete.html'
    queryset = Response.objects.all()
    success_url = '/search_response/'

    permission_required = (
        'fan_forum.view_response',
        'fan_forum.delete_response',
    )


class ResponsesSearchView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'fan_forum/response_search.html'
    context_object_name = 'responses'
    paginate_by = 5

    def get_queryset(self):
        """Возвращает отфильтрованный перечень откликов где автором поста является залогиненный пользователь."""
        queryset = super().get_queryset().filter(post__author__user=self.request.user)
        self.queryset = ResponseFilter(self.request.GET, queryset=queryset)
        return self.queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        return context


class MyResponsesSearchView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'fan_forum/response_my_search.html'
    context_object_name = 'responses'
    paginate_by = 5

    def get_queryset(self):
        """Возвращает отфильтрованный перечень откликов где автором поста является залогиненный пользователь."""
        queryset = super().get_queryset().filter(author=self.request.user.author)
        self.queryset = MyResponseFilter(self.request.GET, queryset=queryset)
        return self.queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        return context


class ResponsesPostView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'fan_forum/responses_post.html'
    context_object_name = 'responses'
    paginate_by = 5

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        user = self.request.user.author

        if user == post.author:
            return Response.objects.filter(post=post).order_by('-datetime_response')
        elif Response.objects.filter(post=post, author=user).exists():
            return Response.objects.filter(Q(post=post, author=user) | Q(post=post, accept=True)).order_by('-datetime_response')
        else:
            return Response.objects.filter(post=post, accept=True).order_by('-datetime_response')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        context['post'] = post

        return context


@login_required
def response_accept(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if not response.accept:
        response.accept = True
        response.save()

        author_response = response.author.user
        post = response.post
        category = post.category.first()
        text_sub = '.'
        category_name = ''

        if category:
            if not category.subscriber.filter(id=author_response.id).exists():
                print('добавили')
                text_sub = ', теперь Вы подписаны на категорию '
                category_name = f'"{category.name}".'
                category.subscriber.add(author_response)

        # Отправка электронного сообщения
        recipient_email = author_response.email
        html_context = render_to_string(
            'email/accept_response.html',
            {
                'cat': category_name,
                'link': f'{SITE_URL}/response/{response.pk}',
                'preview': response.preview(),
                'text_sub': text_sub,

            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Одобрение отклика',
            body='',
            from_email=EMAIL_HOST_USER,
            to=[recipient_email],
        )
        msg.attach_alternative(html_context, 'text/html')
        msg.send()

    return redirect(f'/response/{response_id}/')
