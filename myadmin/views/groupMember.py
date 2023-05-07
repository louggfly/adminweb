# 店铺信息管理的视图文件
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from myadmin.models import Group, myUser, GroupMember


def index(request, pIndex=1):
    '''浏览信息'''
    gmod = GroupMember.objects
    glist = gmod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        glist = glist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        glist = glist.filter(status=status)
        mywhere.append("status=" + status)

    glist = glist.order_by("id")  # 对id排序
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(glist, 10)  # 以每页10条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    for vo in list2:
        uob = myUser.objects.get(id=vo.user_id)
        vo.username = uob.username
        gob = Group.objects.get(id=vo.group_id)
        vo.groupname = gob.name

    context = {"groupmemberlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/groupmember/index.html", context)


def check(request, mid):
    '''浏览信息'''

    gmod = GroupMember.objects.filter(group_id=mid)
    glist = gmod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        glist = glist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        glist = glist.filter(status=status)
        mywhere.append("status=" + status)

    glist = glist.order_by("id")  # 对id排序
    # 执行分页处理
    pIndex = int(1)
    page = Paginator(glist, 10)  # 以每页10条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    for vo in list2:
        uob = myUser.objects.get(id=vo.user_id)
        vo.username = uob.username
        gob = Group.objects.get(id=vo.group_id)
        vo.groupname = gob.name

    context = {"groupmemberlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/groupmember/index.html", context)


def add(request):
    ulist = myUser.objects.values("id", "username")
    ulist = ulist.filter(status=1)
    glist = Group.objects.values("id", "name")
    glist = glist.filter(status=1)
    context = {"userlist": ulist, "grouplist": glist}
    return render(request, "myadmin/groupmember/add.html", context)


def insert(request):
    '''执行信息添加'''
    try:
        ob = GroupMember()
        ob.user_id = request.POST['user_id']
        ob.group_id = request.POST['group_id']
        ob.location = request.POST['location']
        ob.access = 1  # 状态：2:组长 1:成员
        ob.status = 1
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "添加成功！"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, mid):
    '''执行信息删除'''
    try:
        ob = GroupMember.objects.get(id=mid)
        ob.status = 9
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, mid):
    '''加载信息编辑表单'''
    try:
        ob = GroupMember.objects.get(id=mid)
        ulist = myUser.objects.values("id", "username")
        ulist = ulist.filter(status=1)
        glist = Group.objects.values("id", "name")
        glist = glist.filter(status=1)
        context = {"groupmember": ob, "userlist": ulist, "grouplist": glist}
        return render(request, "myadmin/groupmember/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, mid):
    '''执行信息编辑'''
    try:
        ob = GroupMember.objects.get(id=mid)
        ob.user_id = request.POST['user_id']
        ob.group_id = request.POST['group_id']
        ob.location = request.POST['location']
        ob.access = request.POST['access']  # 状态：2:组长 1:成员
        ob.status = 1
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
