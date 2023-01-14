from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

from .forms import PostModelForm
from .models import PostModel

# @login_required


def post_model_create_view(request):
    form = PostModelForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # print(obj.title)
        obj.save()
        messages.success(request, "Created a new blog post!")
        context = {
            "form": PostModelForm()
        }
        return HttpResponseRedirect("/products/")

    template = "products/create-view.html"
    return render(request, template, context)

# @login_required


def post_model_update_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    form = PostModelForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # print(obj.title)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/products/{num}".format(num=obj.id))

    template = "products/update-view.html"
    return render(request, template, context)


def post_model_detail_view(request, id=None):
    # try:
    #     obj = PostModel.objects.get(id=id)
    # except:
    #     raise Http404

    # qs = PostModel.objects.filter(id=id)
    # if not qs.exists() and qs.count!=1:
    #     raise Http404
    # else:
    #     obj = qs.first()

    obj = get_object_or_404(PostModel, id=id)
    context = {
        "object": obj,
    }
    template = "products/detail-view.html"
    return render(request, template, context)


def post_model_delete_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Post deleted")
        return HttpResponseRedirect("/products/")
    context = {
        "object": obj,
    }
    template = "products/delete-view.html"
    return render(request, template, context)


def post_model_list_view(request):
    if request.user.is_authenticated:
        template = "products/list-view.html"
    else:
        template = "products/list-view-public.html"

    #query = request.GET["q"]
    query = request.GET.get("q", None)
    qs = PostModel.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query)
        )
    context = {
        "object_list": qs,
        "messages": ["Hello", "I am doing great", "Sky is blue"]
    }

    return render(request, template, context)


@login_required(login_url='/login/')
def login_required_view(request):
    print(request.user)
    qs = PostModel.objects.all()
    context = {
        "object_list": qs,
    }

    if request.user.is_authenticated:
        template = "products/list-view.html"
    else:
        template = "products/list-view-public.html"
        #raise Http404
        return HttpResponseRedirect("/login")

    return render(request, template, context)


def post_model_robust_view(request, id=None):
    obj = None
    context = {}
    success_message = 'A new post was created'

    if id is None:
        "obj is could be created"
        template = "products/create-view.html"
    else:
        "obj prob exists"
        obj = get_object_or_404(PostModel, id=id)
        success_message = 'A new post was created'
        context["object"] = obj
        template = "products/detail-view.html"
        if "edit" in request.get_full_path():
            template = "products/update-view.html"
        if "delete" in request.get_full_path():
            template = "products/delete-view.html"
            if request.method == "POST":
                obj.delete()
                messages.success(request, "Post deleted")
                return HttpResponseRedirect("/products/")

    # if "edit" in request.get_full_path() or "create" in request.get_full_path():
    form = PostModelForm(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, success_message)
        if obj is not None:
            return HttpResponseRedirect("/products/{num}".format(obj.id))
        context["form"] - PostModelForm()
    return render(request, template, context)
