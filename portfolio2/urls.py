from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import jobs.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", jobs.views.home, name="home"),
    path("blogs/", include("blog.urls")),
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
    path("chatbot/", jobs.views.chatbot_view, name="chatbot"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
