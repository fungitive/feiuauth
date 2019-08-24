from django.shortcuts import render,redirect
from user import models
from .forms import *
from django.db.models import Q
import hashlib
import datetime
from django.conf import settings
from django.core.mail import send_mail
from feiuauth.settings import DEFAULT_FROM_EMAIL
from random import Random


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

# def make_reset_string(email):
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     code = hash_code(email, now)
#     models.ResetString.objects.create(code=code, email=email,)
#     return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.feiutech.com的测试邮件'
    from_email, to = '304719651@qq.com',email
    text_content = '欢迎访问www.feiutech.com，这里是xx站点，专注于xx技术的分享！'
    html_content = '''
                        <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>feiutech菲宇科技</a>，\
                        这里是wo的博客和教程站点，专注于Python和Django技术的分享！</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_info_email(email, code, send_type='register'):
    # new_user = models.User.objects.filter(email=email).first()
    # code = make_confirm_string(new_user)
    # email_record=models.ConfirmString()
    # # email_record.code=code
    # # email_record.user_=email
    # # email_record.send_type=send_type
    # # email_record.save()
    #
    # email_title=''
    # email_body=''

    if send_type=='register':
        email_title='菲宇科技注册激活链接'
        email_body='请点击下面的链接激活你的账号：http://127.0.0.1/confirm/?code={}'.format(code)

        send_status=send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])
        if send_status:
            pass
    elif send_type=='forget':
        email_title = '菲宇科技密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1/reset/?code={}'.format(code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass
# Create your views here.
def index(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        name = request.session.get('user_name')
        user = models.User.objects.get(name=name)
        return render(request,'user/index.html',locals())
    else:
        return redirect('/login/')


def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    # 普通形式
    # if request.method == "POST":
    #     username = request.POST.get('username', None)
    #     password = request.POST.get('password', None)
    #     if username and password:  # 确保用户名和密码都不为空
    #         username = username.strip()
    #         # 用户名字符合法性验证
    #         # 密码长度验证
    #         # 更多的其它验证.....
    #         try:
    #             #实现用户名和邮箱的登录
    #             user = models.User.objects.get(Q(username=username)|Q(email=username))
    #         except:
    #             msg = '用户名或邮箱错误'
    #             return render(request, 'user/login.html',{'msg':msg})
    #         if user.password == password:
    #             return redirect('/index/')
    #         else:
    #             msg = '密码错误'
    #             return render(request, 'user/login.html', {'msg': msg})

    # forms形式
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(Q(name=username)|Q(email=username))
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'user/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    user.ctime = str(datetime.datetime.today())
                    user.save()
                    return redirect('/index/')
                else:
                    msg = '密码错误'
            except:
                msg = '用户名或邮箱错误'
        return render(request, 'user/login.html', locals())
    login_form = UserForm()
    return render(request,'user/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'user/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'user/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'user/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_info_email(email, code, send_type='register')
                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'user/confirm.html', locals())  # 跳转到等待邮件确认页面。
                # return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'user/register.html', locals())

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'user/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'user/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'user/confirm.html', locals())

def forget(request):
    '''忘记密码'''
    if request.method == "GET":
        forget_form=ForgetForm()
        return render(request,'user/forget.html',{'forget_form':forget_form})
    if request.method == "POST":
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email')
            user = models.User.objects.filter(email=email).first()
            if user:
                # print(user.name)
                msg = '重设密码邮件已发送成功，请查收，或在垃圾邮箱查看！'
                code = make_confirm_string(user)
                send_info_email(email, code, 'forget')
                return render(request, 'user/success_send.html', locals())
            else:
                msg='不存在'
                return render(request, 'user/forget.html', {'forget_form': forget_form, 'msg': msg})
            # try:
            #     msg = '重设密码邮件已发送成功，请查收，或在垃圾邮箱查看！'
            #
            #     # print(user)
            #     code = make_confirm_string(user)
            #     print(code)
            #     # send_info_email(email, code, 'forget')
            #     return render(request, 'user/success_send.html', locals())
            # except:
            #     pass
                # msg = '邮箱未注册'
                # return render(request, 'user/forget.html', {'forget_form': forget_form,'msg':msg })

            # code =  models.ConfirmString.objects.get(user=user)
            # print(code)
            # send_info_email(email, code, 'forget')
        else:
            return render(request,'user/forget.html',{'forget_form':forget_form,})

def pwd_reset(request):
    """用户中心主动修改密码"""
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        if request.method == "GET":
            username = request.session.get('user_name')
            print(username)
            reset_form = ResetForm()
            return render(request,'user/pwd_reset.html',locals())
        if request.method == "POST":
            reset_form = ResetForm(request.POST)
            if reset_form.is_valid():
                pwd1 = request.POST.get('newpwd1', '')
                pwd2 = request.POST.get('newpwd2', '')
                username = request.POST.get('username', '')
                if pwd1 != pwd2:
                    return render(request, 'user/pwd_reset.html', {'message': '密码不一致！'})
                else:
                    user = models.User.objects.get(name=username)
                    user.password = hash_code(pwd2)
                    user.save()
                    request.session.flush()
                    return render(request, 'user/pwd_reset_success.html')
    else:
        return redirect("/login/")

def reset(request):
    '''重置密码'''
    if request.method == "GET":
        code = request.GET.get('code')
        reset_form = ResetForm()
        record=models.ConfirmString.objects.filter(code=code)
        if record:
            for i in record:
                user=i.user
                is_register=models.User.objects.filter(name=user)
                if is_register:
                    for j in is_register:
                        email = j.email
                        return render(request,'user/pwd_reset.html',locals())
        return redirect('/')
#因为<form>表单中的路径要是确定的，所以post函数另外定义一个类来完成
    if request.method == "POST":
        code = request.POST.get('code')

        reset_form=ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1=request.POST.get('newpwd1','')
            pwd2=request.POST.get('newpwd2','')
            email=request.POST.get('email','')
            if pwd1!=pwd2:
                return render(request,'user/pwd_reset.html',{'message':'密码不一致！'})
            else:
                user=models.User.objects.get(email=email)
                user.password=hash_code(pwd2)
                user.save()
                record = models.ConfirmString.objects.filter(code=code)
                record.delete()
                return render(request,'user/pwd_reset_success.html')
        else:
            reset_form = ResetForm()
            email=request.POST.get('email','')
            return render(request,'user/pwd_reset.html',locals())

def edit_user(request):
    """用户主动修改资料"""
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        if request.method == "GET":
            name = request.session.get('user_name')
            user = models.User.objects.filter(name=name).first()
            print(user)
            edituserfrom = EditUserForm(user)
            return render(request, 'user/edit_user.html', locals())


from .forms import BookFormSet
from django.shortcuts import render


def manage_books(request):
    if request.method == 'POST':
        formset = BookFormSet(request.POST)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = BookFormSet()
        print(formset)
        # 如果想传入初始数据可设置initial = [{'name':'python','pub_date':'北京出版社'}]
    return render(request, 'manage_books.html', {'formset': formset})