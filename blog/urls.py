from django.urls import path

from . import views

urlpatterns = [
    # path('', views.allblogs, name='blog_list'),
    # path('<int:blog_id>/', views.detail, name='blog_detail'),
    # Class based view
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
