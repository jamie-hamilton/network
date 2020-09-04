from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

"""
# Example of customised model manager:
# https://docs.djangoproject.com/en/3.0/topics/db/managers/
def LondonUserManager(models.Manager):
    def get_queryset(self):
        # 'super' calls pre-existing get_queryset function
        return super(UserManager, self).get_queryset().filter(city="London")

def User(AbstractUser):
    london = LondonUserManager()
    # Calling User.london.all() will now return filtered objects
    # As if calling User.objects.filter(city="London")

# https://www.youtube.com/watch?v=bFhuOULgKDs&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=56
"""

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return f"{self.username}"


class Connect(models.Model):
    following = models.ManyToManyField(User, related_name='followed_by', blank=True)
    current_user = models.OneToOneField(User, related_name='follow_list', on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def follow(cls, current_user, connected_user):
        connection, created = cls.objects.get_or_create(
            current_user=current_user
        )
        connection.following.add(connected_user)

    @classmethod
    def unfollow(cls, current_user, connected_user):
        connection = cls.objects.get(current_user=current_user)
        connection.following.remove(connected_user)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} posted {self.date}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    def __str__(self):
        return f"{self.user.username} liked {self.post.user.username}'s post (#{self.post.id})"


