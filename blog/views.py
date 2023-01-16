from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.utils import timezone

from .models import Blog
from .mixins import TemplateTitleMixin, QuerysetModelMixin


#********************************Function based views**********************************#
# def allblogs(request):
#     blogs = Blog.objects
#     return render(request, 'blog/allblogs.html', {'blogs': blogs})

# def detail(request, blog_id):
#     detailblog = get_object_or_404(Blog, pk=blog_id)
#     return render(request, 'blog/detail.html', {'blog': detailblog})


#********************************Class based views**********************************#


# # Usage of Multiple object mixin
# class BlogObjectMixinListView(MultipleObjectMixin, View):
#     queryset = Blog.objects.filter(pk__gte=0)
#     title = "Blog List"

#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         context = self.get_context_data()
#         app_label = self.object_list.model._meta.app_label
#         model_name = self.object_list.model._meta.model_name
#         template = f"{app_label}/{model_name}_list.html"
#         return render(request, template, context)

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["title"] = "Blog List"
#         return context


# # This view is for better understanding of Listview working principle with mixins
# class BlogUNListView(TemplateTitleMixin, QuerysetModelMixin, View):
#     model = Blog
#     # You can filter whatever you want to pass it to mixin
#     queryset = model.objects.filter(pk__gte=0)
#     title = "Blog List"

#     def get(self, request, *args, **kwargs):
#         template = self.get_template()
#         # context = {
#         #     "object_list": self.get_queryset()
#         # }
#         context = self.get_context_data()
#         return render(request, template, context)


class BlogListView(TemplateTitleMixin, QuerysetModelMixin, ListView):
    model = Blog
    # default template name is 'blog/blog_list.html' it file name is <appname>/<modelname>_list.html
    # template_name = 'blog/blog-list.html'
    # queryset = Blog.objects.order_by('-pub_date')
    # context_object_name = 'blogs'
    title = "Blog List"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        # context["title"] = "Product List Title1"
        # print(context)
        return context

    def get(self, request, *args, **kwargs):
        # do something here and then return
        return super(BlogListView, self).get(request, *args, **kwargs)

    # def get_queryset(self):
    #     # If no queryset variable mentioned, then this will be called
    #     # Do SOMETHING TO FILTER QUERYSET
    #     return Blog.objects.all()
    #     # slug = self.kwargs['slug']
    #     # try:
    #     #     tag = Tag.objects.get(slug=slug)
    #     #     return tag.post_set.all()
    #     # except Tag.DoesNotExist:
    #     #     return Post.objects.none()


# # Using SingleObjectMixin for detail view
# class BlogDetailView(SingleObjectMixin, View):
#     model = Blog
#     # queryset = Blog.objects.filter(pk__gte=0)

#     def get(self, request, *args, **kwargs):
#         print(args, kwargs)
#         object = self.get_object()
#         context = {
#             'blog': object
#         }
#         app_label = self.model._meta.app_label
#         model_name = self.model._meta.model_name
#         template = f"{app_label}/{model_name}_detail.html"
#         return render(request, template, context)


class BlogDetailView(TemplateTitleMixin, DetailView):
    model = Blog
    # default template name is 'blog/blog_detail.html' it file name is <appname>/<modelname>_detail.html
    # template_name = 'blog/detail.html'
    # title = "Blog Detail"  # This title go to mixin to get into context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        # print(context)
        return context

    # if url contains variable name otherthan pk(like id), then need to overide get_object method to get the object
    def get_object(self):
        # print(self.kwargs)
        # This is required if url contains id variable instead of pk
        url_id = self.kwargs.get("id")
        object = self.get_queryset().get(id=url_id)
        return object

    # This is method overiding from mixin to set value of title
    def get_title(self):
        return self.get_object().title
