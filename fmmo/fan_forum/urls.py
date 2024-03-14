from django.urls import path
from .views import *
from .mixins import permission_denied_view, refusal_to_edit_your_post_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostsListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('account/<int:pk>/', PersonalAccountView.as_view(), name='personal_account'),
    path('permission_denied/', permission_denied_view, name='permission_denied'),
    path('refusal_to_edit_your_post/', refusal_to_edit_your_post_view, name='refusal_to_edit_your_post'),
    path('response/<int:pk>/', ResponseDetailView.as_view(), name='response_detail'),
    path('create_response/<int:pk>/', ResponseCreateView.as_view(), name='response_create'),
    path('edit_response/<int:pk>/', ResponseUpdateView.as_view(), name='response_update'),
    path('delete_response/<int:pk>/', ResponseDeleteView.as_view(), name='response_delete'),
    path('search_response/', ResponsesSearchView.as_view(), name='search_responses'),
    path('search_my_response/', MyResponsesSearchView.as_view(), name='search_my_response'),
    path('response_as/<int:response_id>/', response_accept, name='response_accept'),
    path('responses/<int:pk>/', ResponsesPostView.as_view(), name='responses_post'),
]