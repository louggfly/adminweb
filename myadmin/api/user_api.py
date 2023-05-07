import re
from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from adminProject import settings
from myadmin.models import myUser, CommentPicture, Shop, UserFavourite, UserComment

lowerRegex = re.compile('[a-z]')
upperRegex = re.compile('[A-Z]')
digitRegex = re.compile('[0-9]')


# def generate_token(mobile, password):
#     message = mobile + password
#     secret = 'my_secret_key'
#     token = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
#     return token

def generate_token(phone, password):
    payload = {
        'phone': phone,
        'password': password,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


class Register(APIView):
    @staticmethod
    def post(request):
        name = request.data.get('name')
        mobile = request.data.get('phone')
        password = request.data.get('password')
        checkUsername = myUser.objects.filter(username=name)
        checkPhone = myUser.objects.filter(mobile=mobile)
        if checkUsername.exists():
            return Response({'status': 'failed', 'message': '用户名已使用'}, status=status.HTTP_400_BAD_REQUEST)
        elif checkPhone.exists():
            return Response({'status': 'failed', 'message': '电话号码已使用'}, status=status.HTTP_400_BAD_REQUEST)
        elif name == '':
            return Response({'status': 'failed', 'message': '用户名不能为空！'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if len(password) < 8:
                return Response({'status': 'failed', 'message': '添加失败！输入的密码小于8位'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if lowerRegex.search(password) == None:
                    return Response({'status': 'failed', 'message': '添加失败！密码未包含小写字母'},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif upperRegex.search(password) == None:
                    return Response({'status': 'failed', 'message': '添加失败！密码未包含大写字母'},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif digitRegex.search(password) == None:
                    return Response({'status': 'failed', 'message': '添加失败！密码未包含数字'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    ob = myUser()
                    ob.username = name
                    ob.token = generate_token(mobile, password)
                    # 将当前员工信息的密码做md5处理
                    import hashlib, random
                    md5 = hashlib.md5()
                    n = random.randint(100000, 999999)
                    s = password + str(n)  # 从表单中获取密码并添加干扰值
                    md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                    ob.password_hash = md5.hexdigest()  # 获取md5值
                    ob.password_salt = n
                    ob.mobile = mobile
                    ob.status = 1
                    ob.gender = 0
                    ob.area_id = 1
                    ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    ob.save()
                    return Response({'status': 'success', 'token': ob.token}, status=status.HTTP_201_CREATED)


class Login(APIView):
    @staticmethod
    def post(request):
        mobile = request.data.get('phone')
        password = request.data.get('password')
        checkPhone = myUser.objects.filter(mobile=mobile)
        if checkPhone.exists():
            user = myUser.objects.get(mobile=mobile)
            # 判断当前用户是否是管理员
            if user.status == 1:
                # 判断登录密码是否相同
                import hashlib
                md5 = hashlib.md5()
                s = password + user.password_salt  # 从表单中获取密码并添加干扰值
                md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                if user.password_hash == md5.hexdigest():  # 获取md5值
                    print('登录成功')
                    if user.token == "":
                        print('生成token')
                        user.token = generate_token(mobile, password)
                        user.save()
                    return Response({'status': '登录成功', 'token': user.token}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'failed', 'message': '密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'failed', 'message': '用户已注销，请等待管理员操作'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failed', 'message': '电话号码未注册'}, status=status.HTTP_400_BAD_REQUEST)


class NewPassword(APIView):
    @staticmethod
    def post(request):
        mobile = request.data.get('phone')
        password = request.data.get('password')
        checkPhone = myUser.objects.filter(mobile=mobile)
        if checkPhone.exists():
            user = myUser.objects.get(mobile=mobile)
            if user.status == 1:
                if len(password) < 8:
                    return Response({'status': 'failed', 'message': '修改失败！输入的密码小于8位'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    if lowerRegex.search(password) == None:
                        return Response({'status': 'failed', 'message': '修改失败！密码未包含小写字母'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif upperRegex.search(password) == None:
                        return Response({'status': 'failed', 'message': '修改失败！密码未包含大写字母'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif digitRegex.search(password) == None:
                        return Response({'status': 'failed', 'message': '修改失败！密码未包含数字'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        import hashlib, random
                        md5 = hashlib.md5()
                        n = random.randint(100000, 999999)
                        s = password + str(n)  # 从表单中获取密码并添加干扰值
                        md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                        user.password_hash = md5.hexdigest()  # 获取md5值
                        user.password_salt = n
                        user.save()
                    return Response({'status': '密码修改成功'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': '用户已注销，请等待管理员操作'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failed', 'message': '电话号码未注册'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    @staticmethod
    def get(request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        print(token)
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            data = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'mobile': user.mobile,
                'gender': user.gender,
                'introduction': user.introduction,
                'area_id': user.area_id,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '无效的token'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserInfo(APIView):
    @staticmethod
    def post(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            username = request.data.get('username')
            gender = request.data.get('gender')
            introduction = request.data.get('introduction')
            user.username = username
            user.gender = gender
            user.introduction = introduction
            user.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserArea(APIView):
    @staticmethod
    def post(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            areaId = request.data.get('areaId')
            user.area_id = areaId
            user.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAvatar(APIView):
    @staticmethod
    def post(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            imageUrl = request.data.get('imageUrl')
            user.avatar = imageUrl
            user.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserPhone(APIView):
    @staticmethod
    def post(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            newphone = request.data.get('phone')
            user.mobile = newphone
            user.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class AllUser(APIView):
    @staticmethod
    def get(request):
        try:
            users = myUser.objects.filter(status=1)
            data = {
                'usercount': users.count(),
                'users': []
            }
            for user in users:
                data['users'].append({
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'mobile': user.mobile,
                    'gender': user.gender,
                    'introduction': user.introduction,
                    'area_id': user.area_id,
                })
            return Response(data, status=status.HTTP_200_OK)
        except myUser.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class SearchUser(APIView):
    @staticmethod
    def post(request):
        try:
            keyword = request.data.get('keyword')
            users = myUser.objects.filter(username__contains=keyword)
            users = users.filter(status=1)
            data = {
                'usercount': users.count(),
                'users': []
            }
            for user in users:
                data['users'].append({
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'mobile': user.mobile,
                    'gender': user.gender,
                    'introduction': user.introduction,
                    'area_id': user.area_id,
                })
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '用户不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserFavouriteShop(APIView):
    @staticmethod
    def post(request):
        try:
            userId = request.data.get("userId")
            userShop = UserFavourite.objects.filter(user_id=userId)
            userShop = userShop.filter(status=1)
            shops = Shop.objects.filter(status=1)
            data = {
                'shopcount': 0,
                'shops': []
            }
            for item in userShop:
                shop = shops.get(id=item.shop_id)
                data['shops'].append({
                    'id': shop.id,
                    'name': shop.name,
                    'cover_pic': shop.cover_pic,
                    'address': shop.address,
                    'phone': shop.phone,
                    'comments': shop.comments,
                    'grade': shop.grade,
                    'price': shop.price,
                    'opentime': shop.opentime,
                    'share_link': shop.share_link,
                    'keyword': shop.keyword,
                    'area_id': shop.area_id,
                    'category_id': shop.category_id,
                    'time': shop.time
                })
            data['shopcount'] = userShop.count()
            return Response(data, status=status.HTTP_200_OK)
        except UserFavourite.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户收藏不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserFavouriteCreate(APIView):
    @staticmethod
    def post(request):
        try:
            shopId = request.data.get("shopId")
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            ob = UserFavourite()
            ob.user_id = user.id
            ob.shop_id = shopId
            ob.save()
            return Response(status=status.HTTP_200_OK)
        except UserFavourite.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户收藏不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserFavouriteDelete(APIView):
    @staticmethod
    def post(request):
        try:
            shopId = request.data.get("shopId")
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            userShop = UserFavourite.objects.filter(user_id=user.id)
            userShop = userShop.get(shop_id=shopId)
            userShop.status = 9
            userShop.delete()
            return Response(status=status.HTTP_200_OK)
        except UserFavourite.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户收藏不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserCommentList(APIView):
    @staticmethod
    def post(request):
        try:
            user_id = request.data.get("userId")
            comments = UserComment.objects.filter(user_id=user_id)
            comments = comments.filter(status=1)
            comment_data = []
            for comment in comments:
                comment_pictures = CommentPicture.objects.filter(comment_id=comment.id)
                picture_data = []
                for picture in comment_pictures:
                    picture_data.append({
                        'id': picture.id,
                        'comment_id': picture.comment_id,
                        'picture_link': picture.picture_link,
                        'time': picture.time,
                    })
                comment_data.append({
                    'id': comment.id,
                    'shop_id': comment.shop_id,
                    'user_id': comment.user_id,
                    'content': comment.content,
                    'grade': comment.grade,
                    'time': comment.time,
                    'keyword': comment.keyword,
                    'picturecount': comment_pictures.count(),
                    'pictures': picture_data,
                })
            data = {
                'commentcount': comments.count(),
                'comments': comment_data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserComment.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户评论不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    @staticmethod
    def get(request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        print(token)
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            user.status = 9
            user.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '无效的token'}, status=status.HTTP_400_BAD_REQUEST)
