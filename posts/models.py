from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    title = models.CharField(max_length=64)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']



class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
