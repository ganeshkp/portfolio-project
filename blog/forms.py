from django import forms
# from ckeditor.widgets import CKEditorWidget

from .models import Blog
from django.contrib.admin import widgets

# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class BlogModelForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        # fields = '__all__'
        fields = ['title', 'pub_date', "created_datetime", 'body']
        # exclude = ["user"]
        widgets = {
            'pub_date': DateInput(),
            "created_datetime": DateTimeInput,
            # 'body': CKEditorWidget()
        }


# ("db-value", "display-value")
SNACK_CHOICES = [('1', 'Chips'), ('2', 'Bread')]
BREAKFAST_CHOICES = [('1', 'Sandwitch'), ('2', 'Pasta')]
INT_CHOICES = [tuple([x, x]) for x in range(0, 50)]
YEARS = [x for x in range(1980, 2040)]


class TestForm(forms.Form):
    subject = forms.CharField(label="Subject Line",
                              max_length=100, initial="Hi There")
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Sender Email")
    cc_myself = forms.BooleanField(required=False)
    integer = forms.IntegerField(widget=forms.Select(choices=INT_CHOICES))
    date = forms.DateField(initial="2010-01-20",
                           widget=forms.SelectDateWidget(years=YEARS))
    date_time = forms.SplitDateTimeField(
        widget=widgets.AdminTimeWidget)
    snacks = forms.ChoiceField(
        label="Snacks Menu", widget=forms.RadioSelect, choices=SNACK_CHOICES)
    breakfast = forms.CharField(
        label="Breakfast Menu", widget=forms.Select(choices=BREAKFAST_CHOICES))

    # This method can be used to initialize user data automatically for instance
    def __init__(self, user=None, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields["message"].initial = "Can you please help me."
        if user:
            self.fields["sender"].initial = user.email

    def clean_integer(self, *args, **kwargs):
        int_val = self.cleaned_data.get("integer")
        if int_val < 10:
            raise forms.ValidationError("integer must be greater than 10")
        return int_val

    def clean_subject(self, *args, **kwargs):
        subject = self.cleaned_data.get("subject")
        if "shit" in subject:
            raise forms.ValidationError(
                "mean words are not allowed in subject")
        return subject

    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/
    # use this method when Cleaning and validating fields that depend on each other
    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise forms.ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )
