from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list (main page)
    path('', views.PostListView.as_view(), name='post_list'),
    
    # Category filter
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    
    # Post detail
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
