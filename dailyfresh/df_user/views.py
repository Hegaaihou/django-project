#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    if len(uname) == 0 or len(upwd) == 0:
        return redirect('/user/register/')

    #panduanliangcimima
    if upwd != upwd2:
        return redirect('/user/register/')

    #jiami
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')


def register_exist(request):
    get = request.GET
    uname = get.get('uname')
    uobj = UserInfo.objects.filter(uname=uname)
    count = uobj.count()
    if count>1:
        uobj.delete()
    return JsonResponse({'count': count})


def login(request):
    uname=request.COOKIES.get('uname', '')
    context = {'title': 'User Login', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request,'df_user/login.html', context)

def login_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu', 0)

    users=UserInfo.objects.filter(uname=uname)

    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu!=0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': 'UserLogin', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html',context)
    else:
        context = {'title': 'UserLogin', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)
