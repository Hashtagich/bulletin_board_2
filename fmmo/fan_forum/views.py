from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView

from .filters import ResponseFilter, MyResponseFilter
from .forms import PostForm, ResponseForm
from .mixins import AuthorRequiredMixin, AuthorNecessaryMixin
from .models import Post, User, Response


# Create your views here.
class HomeView(TemplateView):  # class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostsListView(ListView):  # class PostsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    ordering = '-datetime_post'
    template_name = 'fan_forum/posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    # permission_required = ('posts.view_post',)


class PostDetailView(DetailView):  # class PostDetail(LoginRequiredMixin, DetailView):
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

    # permission_required = (
    #     'fan_forum.view_response',
    #     'fan_forum.delete_response',
    # )


class ResponsesSearchView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'fan_forum/response_search.html'
    context_object_name = 'responses'
    paginate_by = 5

    # permission_required = ('news.view_post',)

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

    # permission_required = ('news.view_post',)

    def get_queryset(self):
        """Возвращает отфильтрованный перечень откликов где автором поста является залогиненный пользователь."""
        queryset = super().get_queryset().filter(author=self.request.user.author)
        self.queryset = MyResponseFilter(self.request.GET, queryset=queryset)
        return self.queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        return context


@login_required
def response_accept(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if not response.accept:
        response.accept = True
        response.save()

    return redirect(f'/response/{response_id}/')