from django.db import models

# Create your models here.
class Post(models.Model):
    # Postのオーナーを設定する
    owner = models.ForeignKey('accounts.User', verbose_name='オーナー', on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'posts'