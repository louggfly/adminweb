# 店铺信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time
# Create your views here.
from myadmin.models import ShopPicture, Shop


def index(request, pIndex=1):
    '''浏览信息'''
    smod = ShopPicture.objects
    mywhere = []
    list = smod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 10)
    maxpages = page.num_pages
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name

    # 封装信息加载模板输出
    context = {"shoppicturelist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/shoppicture/index.html", context)


def check(request, pid):
    '''浏览信息'''
    smod = ShopPicture.objects.filter(id=pid)
    mywhere = []
    list = smod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(1)
    page = Paginator(list, 10)
    maxpages = page.num_pages
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name

    # 封装信息加载模板输出
    context = {"shoppicturelist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/shoppicture/index.html", context)


def add(request):
    slist = Shop.objects.values("id", "name")
    slist = slist.filter(status=1)
    context = {"shoplist": slist}
    return render(request, "myadmin/shoppicture/add.html", context)


def insert(request):
    '''执行添加'''
    try:
        ob = ShopPicture()
        ob.shop_id = request.POST['shop_id']
        ob.picture_link = request.POST['picture_link']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.status = 1
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, pid):
    '''删除信息'''
    try:
        ob = ShopPicture.objects.get(id=pid)
        ob.status = 9
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}

    return render(request, "myadmin/info.html", context)


def edit(request, pid):
    '''加载编辑信息页面'''
    try:
        ob = ShopPicture.objects.get(id=pid)
        slist = Shop.objects.values("id", "name")
        slist = slist.filter(status=1)
        context = {"shoppicture": ob, "shoplist": slist}
        return render(request, "myadmin/shoppicture/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, pid):
    '''执行编辑信息'''
    try:
        ob = ShopPicture.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.picture_link = request.POST['picture_link']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.status = 1
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)
