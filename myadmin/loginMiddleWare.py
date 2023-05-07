# 自定义中间类（执行是否登录判断）
from django.shortcuts import redirect
from django.urls import reverse
import re


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("LoginMiddleware")

    def __call__(self, request):
        path = request.path
        print("url:", path)

        # 判断管理后台是否登录
        # 定义后台不登录也可直接访问的url列表
        urllist = ['/login', '/logout', '/dologin', '/verify']
        # 判断当前请求url地址不以/api开头
        if not re.match(r"^/api", path):
            # 判断当前请求url地址不在urllist中，才做登录判断
            if path not in urllist:
                # 判断是否登录(在于session中没有adminuser)
                if 'adminuser' not in request.session:
                    # 重定向到登录页
                    return redirect(reverse("myadmin_login"))
                    # pass

        response = self.get_response(request)
        return response
