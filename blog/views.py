from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
import json
from django.forms import formset_factory, modelformset_factory
from django.db.models import Q
from .tasks import send_blog_mail


from django.views.generic import (
    View,
    ListView,
    DetailView,
    RedirectView,
    CreateView,
    UpdateView,
    DeleteView)

from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, Http404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BlogModelForm, TestForm
from .models import Blog
from .mixins import TemplateTitleMixin, QuerysetModelMixin, MyLoginRequiredMixin
from django.views.generic.edit import FormMixin, ModelFormMixin


def formset_view(request):
    if request.user.is_authenticated:
        BlogModelFormset = modelformset_factory(
            Blog, form=BlogModelForm, extra=0)  # extra=2 means create 2 additional empty forms
        formset = BlogModelFormset(request.POST or None,
                                   queryset=Blog.objects.filter(user=request.user))
        if formset.is_valid():
            # formset.save(commit=False)
            for form in formset:
                print(form.cleaned_data)
                obj = form.save(commit=False)
                if form.cleaned_data:
                    #obj.title = "This title %s" %(obj.id)
                    if not form.cleaned_data.get("publish"):
                        obj.publish = timezone.now()
                    obj.save()
            # return redirect("/")
                # print(form.cleaned_data)
        context = {
            "formset": formset
        }
        return render(request, "formset_view.html", context)
    else:
        raise Http404

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

    def get_queryset(self):
        # return self.model.objects.filter(user=self.request.user)
        query = self.request.GET.get("q", None)
        if self.request.user.pk:
            qs = self.model.objects.filter(user=self.request.user)
        else:
            qs = self.model.objects.none()
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            )
        return qs

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


# Using RedirectView
class BlogRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'blog_detail'

    # def get_redirect_url(self, *args, **kwargs):
    #     # blog = get_object_or_404(Blog, pk=kwargs['id'])
    #     return super().get_redirect_url(*args, **kwargs)


# class BlogDetailView(TemplateTitleMixin, MyLoginRequiredMixin, DetailView):
# class BlogDetailView(TemplateTitleMixin, LoginRequiredMixin, DetailView):
class BlogDetailView(LoginRequiredMixin, TemplateTitleMixin, DetailView):
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

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class MyBlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogModelForm
    # template_name = 'forms.html'
    template_name = "blog/blog_form.html"
    # success_url = '/blogs'

    def get_initial(self):
        return {}

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.user = self.request.user
        obj.save()
        # send_blog_mail.delay("ganeshkp3006@gmail.com", "This is content")
        return super().form_valid(form)

    # This method can be used if form go invalid
    def form_invalid(self, form):
        # print(form.errors.as_json())
        # print(dir(form.errors))
        for key, val in form.errors.items():
            # print(key, ":", json.loads(val.as_json())[0]["message"])
            # print(key, ":", val.as_data()[0].messages[0])
            print(key, ":", val.as_text())
        return super().form_invalid(form)


class MyBlogBaseFormView(LoginRequiredMixin, FormMixin, View):
    form_class = BlogModelForm
    template_name = 'forms.html'
    # success_url = '/blogs'

    def get(self, request, *args, **kwargs):
        form = self.get_form()  # This can be used since we are using FormMixin
        return render(request, self.template_name, {"form": form})

    def get_initial(self):
        return {"title": "Hello world"}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    # This method can be used if form go invalid
    def form_invalid(self, form):
        return super().form_invalid(form)


class MyBlogBaseModelFormView(LoginRequiredMixin, ModelFormMixin, View):
    form_class = BlogModelForm
    template_name = 'forms.html'
    # success_url = '/blogs'

    def get(self, request, *args, **kwargs):
        form = self.get_form()  # This can be used since we are using FormMixin
        return render(request, self.template_name, {"form": form})

    def get_initial(self):
        return {"title": "Hello world"}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # This method can be used if form go invalid
    def form_invalid(self, form):
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogModelForm
    # login_url = '/login/'
    # redirect_field_name = 'forms.html'
    template_name = "blog/blog_detail.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        # return f"/blogs/{self.object.id}/"
        # return self.object.get_absolute_url() # This is not working somehow
        return reverse('blog_detail', kwargs={'id': self.object.id})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')
    # by default we need to create template blog/blog_confirm_delete.html if below line is not mentioned
    template_name = "forms-delete.html"


# https://docs.djangoproject.com/en/4.1/topics/forms/#building-a-form-in-django
def test_form_view(request):
    # initial_dict = {
    #     "subject": "Hi There"
    # }

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # form = TestForm(request.POST or None, initial=initial_dict)
        form = TestForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/blogs/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TestForm(user=request.user)
    return render(request, "forms.html", {"form": form})
