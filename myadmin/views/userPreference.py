from django.core.paginator import Paginator
from django.shortcuts import render

from myadmin.models import UserPreference, myUser, Shop, ShopCategory


# 菜品分类信息

def index(request, pIndex=1):
    '''浏览信息'''
    smod = UserPreference.objects
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
        uob = myUser.objects.get(id=vo.user_id)
        vo.username = uob.username
        cob = ShopCategory.objects.get(id=vo.category_id)
        vo.category = cob.name

    # 封装信息加载模板输出
    context = {"preferencelist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/userpreference/index.html", context)


def add(request):
    '''加载添加页面'''
    ulist = myUser.objects.values("id", "username")
    ulist = ulist.filter(status=1)
    clist = ShopCategory.objects.values("id", "name")
    clist = clist.filter(status=1)
    context = {"userlist": ulist, "categorylist": clist}
    return render(request, "myadmin/userpreference/add.html", context)


def insert(request):
    '''执行添加'''
    try:
        ob = UserPreference()
        ob.user_id = request.POST['user_id']
        ob.category_id = request.POST['category_id']
        ob.status = 1
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid):
    '''删除信息'''
    try:
        ob = UserPreference.objects.get(id=uid)
        ob.status = 9
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}

    return render(request, "myadmin/info.html", context)


def edit(request, uid):
    '''加载编辑信息页面'''
    try:
        ob = UserPreference.objects.get(id=uid)
        ulist = myUser.objects.values("id", "username")
        ulist = ulist.filter(status=1)
        clist = ShopCategory.objects.values("id", "name")
        clist = clist.filter(status=1)
        context = {"userpreference": ob, "userlist": ulist, "categorylist": clist}
        return render(request, "myadmin/userpreference/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, uid):
    '''执行编辑信息'''
    try:
        ob = UserPreference.objects.get(id=uid)
        ob.category_id = request.POST['category_id']
        ob.user_id = request.POST['user_id']
        ob.status = 1
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)
