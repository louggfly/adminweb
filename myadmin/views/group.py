# 店铺信息管理的视图文件
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from myadmin.models import Group, myUser, Shop, GroupMember


def index(request, pIndex=1):
    '''浏览信息'''
    gmod = Group.objects
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
        uob = myUser.objects.get(id=vo.leader_id)
        vo.username = uob.username
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name

    context = {"grouplist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/group/index.html", context)


def add(request):
    ulist = myUser.objects.values("id", "username")
    ulist = ulist.filter(status=1)
    slist = Shop.objects.values("id", "name")
    slist = slist.filter(status=1)
    context = {"userlist": ulist, "shoplist": slist}
    return render(request, "myadmin/group/add.html", context)


def insert(request):
    '''执行信息添加'''
    try:
        ob = Group()
        ob.name = request.POST['name']
        ob.shop_id = request.POST['shop_id']
        ob.leader_id = request.POST['leader_id']
        ob.share_link = request.POST['share_link']
        ob.status = 1
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.reserve_at = datetime.strptime(request.POST['reserve_at'], '%Y-%m-%dT%H:%M')
        ob.save()
        mb = GroupMember()
        mb.user_id = ob.leader_id
        mb.group_id = ob.id
        mb.access = 2  # 状态：2:组长 1:成员
        mb.status = 1
        mb.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        mb.save()
        context = {'info': "添加成功！"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, gid):
    '''执行信息删除'''
    try:
        ob = Group.objects.get(id=gid)
        ob.status = 9
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, gid):
    '''加载信息编辑表单'''
    try:
        ob = Group.objects.get(id=gid)
        ulist = GroupMember.objects
        ulist = ulist.filter(status=1, group_id=gid)
        for vo in ulist:
            uob = myUser.objects.get(id=vo.user_id)
            vo.username = uob.username
        slist = Shop.objects.values("id", "name")
        slist = slist.filter(status=1)
        context = {"group": ob, "userlist": ulist, "shoplist": slist}
        return render(request, "myadmin/group/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, gid):
    '''执行信息编辑'''
    try:
        ob = Group.objects.get(id=gid)
        formerLeader = ob.leader_id
        newLeader = request.POST['leader_id']
        ob.name = request.POST['name']
        ob.shop_id = request.POST['shop_id']
        ob.leader_id = request.POST['leader_id']
        ob.share_link = request.POST['share_link']
        ob.status = 1
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.reserve_at = datetime.strptime(request.POST['reserve_at'], '%Y-%m-%dT%H:%M')
        fl = GroupMember.objects.get(user_id=formerLeader, group_id=gid)
        fl.access = 1
        nl = GroupMember.objects.get(user_id=newLeader, group_id=gid)
        nl.access = 2
        nl.save()
        fl.save()
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
