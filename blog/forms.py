from django import forms
# from ckeditor.widgets import CKEditorWidget

from .models import Blog

# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django


class DateInput(forms.DateInput):
    input_type = 'date'


class BlogModelForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'
        # fields = [
        #     'title',
        #     'pub_date',
        #     'body'
        # ]
        widgets = {
            'pub_date': DateInput(),
            # 'body': CKEditorWidget()
        }
