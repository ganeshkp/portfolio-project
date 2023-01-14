from django.urls import re_path


from .views import (
    post_model_create_view,
    post_model_detail_view,
    post_model_delete_view,
    post_model_list_view,
    post_model_update_view
)

urlpatterns = [
    re_path(r'^$', post_model_list_view, name='post-list'),
    re_path(r'^create/$', post_model_create_view, name='post-create'),
    re_path(r'^(?P<id>\d+)/$', post_model_detail_view, name='post-detail'),
    re_path(r'^(?P<id>\d+)/delete/$',
            post_model_delete_view, name='post-delete'),
    re_path(r'^(?P<id>\d+)/edit/$', post_model_update_view, name='post-update'),
    #url(r'^admin/', admin.site.urls),
    #url(r'^$', home, name='home'),
    #url(r'^redirect/$', redirect_somewhere, name='home')
]
