# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
# Create your views here.
from myadmin.models import Admin
import re

# 密码检测格式
lowerRegex = re.compile('[a-z]')
upperRegex = re.compile('[A-Z]')
digitRegex = re.compile('[0-9]')


def index(request, pIndex=1):
    '''浏览信息'''
    umod = Admin.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    ulist = ulist.order_by("id")  # 对id排序
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"adminlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/admin/index.html", context)


def add(request):
    '''加载信息添加表单'''
    return render(request, "myadmin/admin/add.html")


def insert(request):
    '''执行信息添加'''
    try:
        checkUsername = Admin.objects.filter(username=request.POST['username'])
        checkNickname = Admin.objects.filter(nickname=request.POST['nickname'])
        password = request.POST['password']
        repassword = request.POST['repassword']
        username = request.POST['username']
        nickname = request.POST['nickname']
        if checkUsername.exists():
            context = {'info': "用户已存在！添加失败！"}
        elif username == '':
            context = {'info': "管理员账号不能为空！"}
        elif nickname == '':
            context = {'info': "用户昵称不能为空！"}
        else:
            if checkNickname.exists():
                context = {'info': "昵称已被使用！添加失败！"}
            else:
                if len(password) < 8:
                    context = {'info': "添加失败！输入的密码小于8位"}
                else:
                    if lowerRegex.search(password) == None:
                        context = {'info': "添加失败！未包含小写字母"}
                    elif upperRegex.search(password) == None:
                        context = {'info': "添加失败！未包含大写字母"}
                    elif digitRegex.search(password) == None:
                        context = {'info': "添加失败！未包含数字"}
                    elif repassword != password:
                        context = {'info': "添加失败！两次密码输入不一致！"}
                    else:
                        ob = Admin()
                        ob.username = request.POST['username']
                        ob.nickname = request.POST['nickname']
                        # 将当前员工信息的密码做md5处理
                        import hashlib, random
                        md5 = hashlib.md5()
                        n = random.randint(100000, 999999)
                        s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
                        md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                        ob.password_hash = md5.hexdigest()  # 获取md5值
                        ob.password_salt = n
                        ob.status = 1
                        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
                        ob.save()
                        context = {'info': "添加成功！"}

    except Exception as err:
        print(err)
        context = {'info': "未知错误！添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = Admin.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    '''加载信息编辑表单'''
    try:
        ob = Admin.objects.get(id=uid)
        context = {'admin': ob}
        return render(request, "myadmin/admin/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, uid):
    '''执行信息编辑'''
    try:
        checkNickname = Admin.objects.filter(nickname=request.POST['nickname'])
        if checkNickname.exists():
            context = {'info': "昵称已被使用！添加失败！"}
        else:
            ob = Admin.objects.get(id=uid)
            ob.nickname = request.POST['nickname']
            ob.status = request.POST['status']
            ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            ob.save()
            context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
