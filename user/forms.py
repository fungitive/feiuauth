from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',)

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


#forget.html中，用于验证邮箱格式和验证码
class ForgetForm(forms.Form):
    email=forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}),required=True)
    captcha=CaptchaField(label='验证码',error_messages={'invalid':'验证码错误'})

#reset.html中，用于验证新设的密码长度是否达标
class ResetForm(forms.Form):
    newpwd1=forms.CharField(label='设置新密码',required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"},widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newpwd2 = forms.CharField(label='再输入一次',required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"}, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#修改用户资料
class EditUserForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False,disabled=True)
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,disabled=True)
    sex = forms.ChoiceField(label='性别', choices=gender,disabled=True)
    nickname = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}),required=True,)
    avatar =forms.ImageField(label='头像')


from django.forms import formset_factory
from django import forms


class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField()
    pub_date = forms.DateField(required=False)


BookFormSet = formset_factory(BookForm, extra=3, max_num=2)

bbb=formset_factory()