from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import jobs.views
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jobs.views.home, name='home'),
    path('blogs/', include('blog.urls')),
    path('products/', include('products.urls')),
    path('accounts/login/', views.LoginView.as_view(),
         name='login', kwargs={'next_page': '/'}),
    path('accounts/logout/', views.LogoutView.as_view(),
         name='logout', kwargs={'next_page': '/'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
