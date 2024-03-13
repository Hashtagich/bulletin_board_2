from django.shortcuts import get_object_or_404
from django.shortcuts import render


class AuthorRequiredMixin:
    """Класс для проверки того что залогиненный пользователь является автором данной публикации.
    Для работы в классе-наследнике нужно указать переменную model_search, имеющую аргумент author."""

    def dispatch(self, request, *args, **kwargs):
        """Метод проверяет является залогиненный пользователь автором публикации или нет.
        Да - возвращает родительский метод dispatch.
        Нет - выдаёт страницу с отказом доступа через функцию permission_denied_view."""
        model = self.model_search
        post = get_object_or_404(model, pk=kwargs['pk'])
        if request.user.author != post.author:
            return permission_denied_view(request)
        return super().dispatch(request, *args, **kwargs)


class AuthorNecessaryMixin:
    """Класс для проверки того что залогиненный пользователь является автором данной публикации.
    Для работы в классе-наследнике нужно указать переменную model_search, имеющую аргумент author."""

    def dispatch(self, request, *args, **kwargs):
        """Метод проверяет является залогиненный пользователь автором публикации или нет.
        Нет - возвращает родительский метод dispatch.
        Да - выдаёт страницу с отказом доступа через функцию permission_denied_view."""
        model = self.model_search
        post = get_object_or_404(model, pk=kwargs['pk'])
        if request.user.author == post.author:
            return refusal_to_edit_your_post_view(request)
        return super().dispatch(request, *args, **kwargs)


def permission_denied_view(request):
    """Вызов страницы с отображением информации в отказе доступа к странице."""
    return render(request, 'flatpages/permission_denied.html')


def refusal_to_edit_your_post_view(request):
    """Вызов страницы с отображением информации в отказе доступа к странице при попытке написать отклик самому себе."""
    return render(request, 'flatpages/refusal_to_edit_your_post.html')