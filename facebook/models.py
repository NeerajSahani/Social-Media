from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
from django.utils.text import slugify

# Few Queries
# Friend List : person_instance.friend_list.all()
# New Friend Requests : FriendRequest.objects.filter(receiver=person_instance, seen=False)
# New Received Messages : user_instance.message_receiver.filter(seen=False)
# Groups : user_instance.group.all()

GENDER_CHOICES = [
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other')
]


class Person(User):
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    slug = models.SlugField(editable=False)
    about = models.CharField(max_length=255, help_text="maximum 255 characters")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10, help_text="Don't include country code")
    friend_list = models.ManyToManyField("Person", related_name='friends')
    image = models.ImageField(upload_to='profiles', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class FriendRequest(models.Model):
    sender = models.ForeignKey(Person, related_name='request_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Person, related_name='request_receiver', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, editable=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'<sender: {self.sender.slug}, receiver: {self.receiver.slug}>'


ACCESS_CHOICES = [
    ('public', 'Everyone'),
    ('private', 'Friends')
]


class Groups(models.Model):
    title = models.CharField(max_length=20, default='Group')
    slug = models.SlugField(editable=False)
    admin = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='group_admin')
    members = models.ManyToManyField(Person, related_name='group')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to='groups', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    visible_to = models.CharField(max_length=10, choices=ACCESS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ManyToManyField(Groups)

    def __str__(self):
        return f'<{self.author}: {self.title}>'


class Message(models.Model):
    sender = models.ForeignKey(
        Person,
        related_name='message_sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Person,
        related_name='message_receiver',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    seen = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE)
    header = models.CharField(max_length=50, default='New notification')
    body = models.TextField()
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'*{self.header}' if not self.seen else f'{self.header}'
