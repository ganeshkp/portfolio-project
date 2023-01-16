

# Title mixin
class TemplateTitleMixin(object):
    """
    Multiple object mixin
    """
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_title()
        return context

    def get_title(self):
        return self.title


class QuerysetModelMixin():
    model = None
    queryset = None

    def get_template(self):
        if self.model is None:
            raise Exception("You need to set a model")
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        return f"{app_label}/{model_name}_list.html"

    def get_queryset(self):
        qs = None
        if self.queryset is not None:
            qs = self.queryset
            self.model = qs.model
        elif self.model is not None:
            qs = self.model.objects.all()
        else:
            raise Exception("You need to specify a model")
        return qs

    def get_context_data(self):
        context = {
            "object_list": self.get_queryset()
        }
        return context
