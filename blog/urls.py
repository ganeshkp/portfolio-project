from django.urls import path

from . import views

urlpatterns = [
    # path('', views.allblogs, name='blog_list'),
    # path('<int:blog_id>/', views.detail, name='blog_detail'),
    # Class based view
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog<int:id>/', views.BlogRedirectView.as_view(),
         name='blog_detail_redirect'),
    path('<int:id>/', views.BlogDetailView.as_view(), name='blog_detail'),
    # path('create/', views.MyBlogCreateView.as_view(), name='blog_create'),
    # path('create/', views.MyBlogBaseFormView.as_view(), name='blog_create'),
    path('create/', views.MyBlogBaseModelFormView.as_view(), name='blog_create'),
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),

    path('testform/', views.test_form_view, name="test_form"),



]
