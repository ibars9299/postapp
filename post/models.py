from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

from django.contrib.auth.models import User

class Login(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Kullanıcıya bağlı
    # Ekstra bilgiler eklemek isterseniz burada yeni alanlar tanımlayabilirsiniz
    # Örneğin: email, profile picture gibi.

    def __str__(self):
        return self.user.username
    
class Register(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    def __str__(self):
        return self.username
