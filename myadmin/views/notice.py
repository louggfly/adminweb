from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

from myadmin.models import UserComment, myUser, Shop, Notice, Admin


# 菜品分类信息

def index(request, pIndex=1):
    smod = Notice.objects
    mywhere = []
    list = smod.filter(status__lt=9)

    kw = request.GET.get("keyword", None)
    if kw:
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    pIndex = int(pIndex)
    page = Paginator(list, 10)
    maxpages = page.num_pages

    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    for vo in list2:
        aob = Admin.objects.get(id=vo.admin_id)
        vo.username = aob.username

    # 封装信息加载模板输出
    context = {"noticelist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/notice/index.html", context)


def add(request):
    '''加载添加页面'''
    alist = Admin.objects.values("id", "username")
    alist = alist.filter(status=1)
    context = {"adminlist": alist}
    return render(request, "myadmin/notice/add.html", context)


def insert(request):
    '''执行添加'''
    try:
        ob = Notice()
        ob.admin_id = request.POST['admin_id']
        ob.title = request.POST['title']
        ob.content = request.POST['content']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.status = 1
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, nid):
    '''删除信息'''
    try:
        ob = Notice.objects.get(id=nid)
        ob.status = 9
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}

    return render(request, "myadmin/info.html", context)


def edit(request, nid):
    '''加载编辑信息页面'''
    try:
        ob = Notice.objects.get(id=nid)
        alist = Admin.objects.values("id", "username")
        alist = alist.filter(status=1)
        context = {"notice": ob, "adminlist": alist}
        return render(request, "myadmin/notice/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, nid):
    '''执行编辑信息'''
    try:
        ob = Notice.objects.get(id=nid)
        ob.admin_id = request.POST['admin_id']
        ob.title = request.POST['title']
        ob.content = request.POST['content']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.status = 1
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)
