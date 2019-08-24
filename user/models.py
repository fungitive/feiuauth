from django.db import models

# Create your models here.

class User(models.Model):
    '''用户表'''

    gender = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(max_length=128,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    nickname = models.CharField(max_length=128,blank=True,null=True,verbose_name='昵称')
    avatar =models.ImageField(blank=True,null=True)
    atime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    ctime = models.DateTimeField(verbose_name='最后登录时间',auto_now=True)
    has_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['atime']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    """确认码"""
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

# class ResetString(models.Model):
#     """验证码"""
#     code = models.CharField(max_length=256)
#     email = models.EmailField(unique=True)
#     c_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.email + ":   " + self.code
#
#     class Meta:
#         ordering = ["-c_time"]
#         verbose_name = "验证码"
#         verbose_name_plural = "验证码"