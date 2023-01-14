from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.utils import timezone

from .models import Blog


# def allblogs(request):
#     blogs = Blog.objects
#     return render(request, 'blog/allblogs.html', {'blogs': blogs})


def detail(request, blog_id):
    detailblog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog': detailblog})


# Class based view
class BlogListView(ListView):
    model = Blog
    # default template name is 'blog/blog_list.html' it file name is <appname>/<modelname>_list.html
    # template_name = 'blog/allblogs.html'
    queryset = Blog.objects.order_by('-pub_date')
    # context_object_name = 'blogs'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        context["title"] = "Product List Title"
        print(context)
        return context


class BlogDetailView(DetailView):
    model = Blog
    # default template name is 'blog/blog_detail.html' it file name is <appname>/<modelname>_detail.html
    # template_name = 'blog/detail.html'
