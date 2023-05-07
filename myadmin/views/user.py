# 会员信息管理的视图文件
import re
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from myadmin.models import myUser, Area

lowerRegex = re.compile('[a-z]')
upperRegex = re.compile('[A-Z]')
digitRegex = re.compile('[0-9]')


def index(request, pIndex=1):
    '''浏览信息'''
    umod = myUser.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword=' + kw)
    # 判断并处理状态搜索条件
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

    for vo in list2:
        aob = Area.objects.get(id=vo.area_id)
        vo.area = aob.name

    context = {"userlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/user/index.html", context)


def add(request):
    alist = Area.objects.values("id", "name")
    alist = alist.filter(status=1)
    context = {"arealist": alist}
    return render(request, "myadmin/user/add.html", context)


def insert(request):
    '''执行信息添加'''
    try:
        checkUsername = myUser.objects.filter(username=request.POST['username'])
        password = request.POST['password']
        repassword = request.POST['repassword']
        username = request.POST['username']
        if checkUsername.exists():
            context = {'info': "用户已存在！添加失败！"}
        elif username == '':
            context = {'info': " 用户名不能为空！"}
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
                    ob = myUser()
                    ob.username = request.POST['username']
                    # 将当前员工信息的密码做md5处理
                    import hashlib, random
                    md5 = hashlib.md5()
                    n = random.randint(100000, 999999)
                    s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
                    md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                    ob.password_hash = md5.hexdigest()  # 获取md5值
                    ob.password_salt = n
                    ob.status = 1
                    ob.gender = 0
                    ob.area_id = request.POST['area_id']
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
        ob = myUser.objects.get(id=uid)
        ob.status = 9
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    '''加载信息编辑表单'''
    try:
        ob = myUser.objects.get(id=uid)
        alist = Area.objects.values("id", "name")
        alist = alist.filter(status=1)
        context = {"arealist": alist, 'user': ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, uid):
    '''执行信息编辑'''
    try:
        checkUsername = myUser.objects.filter(username=request.POST['username'])
        if checkUsername.count() == 2:
            context = {'info': "昵称已被使用！添加失败！"}
        else:
            ob = myUser.objects.get(id=uid)
            ob.username = request.POST['username']
            ob.avatar = request.POST['avatar']
            ob.mobile = request.POST['mobile']
            ob.introduction = request.POST['introduction']
            ob.status = request.POST['status']
            ob.gender = request.POST['gender']
            ob.area_id = request.POST['area_id']
            ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            ob.save()
            context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
