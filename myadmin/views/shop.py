# 店铺信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time
# Create your views here.
from myadmin.models import Shop, Area, ShopCategory, UserComment


def index(request, pIndex=1):
    '''浏览信息'''
    smod = Shop.objects
    slist = smod.filter(status__lt=9)
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)

    slist = slist.order_by("id")  # 对id排序
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(slist, 5)  # 以每页5条数据分页
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
        cob = ShopCategory.objects.get(id=vo.category_id)
        vo.category = cob.name

    context = {"shoplist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/shop/index.html", context)


def add(request):
    alist = Area.objects.values("id", "name")
    alist = alist.filter(status=1)
    clist = ShopCategory.objects.values("id", "name")
    clist = clist.filter(status=1)
    context = {"arealist": alist, "categorylist": clist}
    return render(request, "myadmin/shop/add.html", context)


def insert(request):
    '''执行信息添加'''
    try:
        # 实例化model，封装信息，并执行添加操作
        ob = Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.cover_pic = request.POST['cover_pic']
        ob.status = 1
        ob.comments = 0
        ob.grade = 0
        ob.price = request.POST['price']
        ob.opentime = request.POST['opentime']
        ob.share_link = request.POST['share_link']
        ob.keyword = request.POST['keyword']
        ob.area_id = request.POST['area_id']
        ob.category_id = request.POST['category_id']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "添加成功！"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, sid=0):
    '''执行信息删除'''
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, sid=0):
    '''加载信息编辑表单'''
    try:
        ob = Shop.objects.get(id=sid)
        alist = Area.objects.values("id", "name")
        alist = alist.filter(status=1)
        clist = ShopCategory.objects.values("id", "name")
        clist = clist.filter(status=1)
        context = {'shop': ob, "arealist": alist, "categorylist": clist}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, sid):
    '''执行信息编辑'''
    try:
        cob = UserComment.objects.filter(shop_id=sid)
        total = 0
        for vo in cob:
            total += vo.grade
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.cover_pic = request.POST['cover_pic']
        ob.status = 1
        ob.comments = cob.count()
        if cob.count() == 0:
            ob.grade = 0
        else:
            ob.grade = total / cob.count()
        ob.price = request.POST['price']
        ob.opentime = request.POST['opentime']
        ob.share_link = request.POST['share_link']
        ob.keyword = request.POST['keyword']
        ob.area_id = request.POST['area_id']
        ob.category_id = request.POST['category_id']
        ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)
