from .validators import validate_author_email, validate_justin
from datetime import timedelta, datetime, date
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.encoding import smart_str
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince


# Create your models here.
User = settings.AUTH_USER_MODEL


class PostModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def post_title_items(self, value):
        return self.filter(title__icontains=value)


class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        # qs = super(PostModelManager, self).all(*args, **kwargs).active() #.filter(active=True)
        # print(qs)
        qs = self.get_queryset().active()
        return qs

    def get_timeframe(self, date1, date2):
        # assume datetime objects
        qs = self.get_queryset()
        qs_time_1 = qs.filter(publish_date__gte=date1)
        qs_time_2 = qs_time_1.filter(publish_date__lt=date2)  # Q Lookups
        #final_qs = (qs_time_1 | qs_time_2).distinct()
        return qs_time_2


class PostModel(models.Model):
    # DRAFT = "DR"
    # PUBLISH = "PU"
    # PRIVATE = "PR"
    # PUBLISH_CHOICES = [
    #     (DRAFT, 'Draft'),
    #     (PUBLISH, 'Publish'),
    #     (PRIVATE, 'Private'),
    # ]
    class PostPublushOptions(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISH = "PU", "Publish"
        PRIVATE = "PR", "Private"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, )
    active = models.BooleanField(default=True)  # empty in the database
    title = models.CharField(
        max_length=240,
        verbose_name='Post title',
        unique=True,
        error_messages={
            "unique": "This title is not unique, please try again.",
            "blank": "This field is not full, please try again."
        },
        help_text='Must be a unique title.')
    slug = models.SlugField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    publish = models.CharField(
        max_length=2, choices=PostPublushOptions.choices, default=PostPublushOptions.DRAFT)
    view_count = models.IntegerField(default=0)
    publish_date = models.DateField(
        auto_now=False, auto_now_add=False, default=timezone.now)  # check usage of timezone here..it is not now()
    author_email = models.EmailField(max_length=240, validators=[
                                     validate_justin, validate_author_email], null=True, blank=True)
    # auto set when object was last saved
    updated = models.DateTimeField(auto_now=True)
    # autoset when object is created
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostModelManager()
    other = PostModelManager()
    #save = PostModelManager()

    def save(self, *args, **kwargs):
        # if not self.slug and self.title:
        #     self.slug = slugify(self.title)
        super(PostModel, self).save(*args, **kwargs)

    def clean(self):
        pass

    class Meta:
        # ordering = ["title"]
        # ordering = ["-title"]  # reverse ordering
        # db_table = '<appname>_<modelname>'  # by default
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        #unique_together = [('title', 'slug')]

    def __unicode__(self):  # python 2
        return smart_str(self.title)  # self.title

    def __str__(self):  # python 3
        return smart_str(self.title)

    @property
    def age(self):
        if self.publish == 'publish':
            now = datetime.now()
            publish_time = datetime.combine(
                self.publish_date,
                datetime.now().min.time()
            )
            try:
                difference = now - publish_time
            except:
                return "Unknown"
            if difference <= timedelta(minutes=1):
                return 'just now'
            return '{time} ago'.format(time=timesince(publish_time).split(', ')[0])
        return "Not published"


def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print("before save")
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)


pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)


def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print("after save")
    print(created)
    if created:
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
            instance.save()


post_save.connect(blog_post_model_post_save_receiver, sender=PostModel)


'''
python manage.py makemigrations #every time you change models.py
python manage.py migate


ModelForm
forms.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')

'''
