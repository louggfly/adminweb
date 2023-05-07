import random

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from adminProject import settings
from myadmin.models import Shop, UserComment, CommentPicture, myUser, UserPreference


class AllShop(APIView):
    @staticmethod
    def get(request):
        try:
            shops = Shop.objects.filter(status=1)
            data = {
                'shopcount': shops.count(),
                'shops': []
            }
            for shop in shops:
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
            return Response(data, status=status.HTTP_200_OK)
        except Shop.DoesNotExist:
            return Response({'status': 'failed', 'message': '店铺不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class SearchShop(APIView):
    @staticmethod
    def post(request):
        try:
            keyword = request.data.get('keyword')
            shops = Shop.objects.filter(name__contains=keyword)
            shops = shops.filter(status=1)
            data = {
                'shopcount': shops.count(),
                'shops': []
            }
            for shop in shops:
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
            return Response(data, status=status.HTTP_200_OK)
        except Shop.DoesNotExist:
            return Response({'status': 'failed', 'message': '餐厅不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class QueryShop(APIView):
    @staticmethod
    def post(request):
        try:
            shop_id = request.data.get("shopId")
            shop = Shop.objects.get(id=shop_id)
            data = {
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
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '店铺不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class QueryShopCommentList(APIView):
    @staticmethod
    def post(request):
        try:
            shop_id = request.data.get("shopId")
            comments = UserComment.objects.filter(shop_id=shop_id)
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
        except:
            return Response({'status': 'failed', 'message': '店铺不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class QueryShopComment(APIView):
    @staticmethod
    def post(request):
        try:
            comment_id = request.data.get("commentId")
            comment = UserComment.objects.get(id=comment_id)
            comment_pictures = CommentPicture.objects.filter(comment_id=comment_id)
            picture_data = []
            for picture in comment_pictures:
                picture_data.append({
                    'id': picture.id,
                    'comment_id': picture.comment_id,
                    'picture_link': picture.picture_link,
                    'time': picture.time,
                })
            data = {
                'id': comment.id,
                'shop_id': comment.shop_id,
                'user_id': comment.user_id,
                'content': comment.content,
                'grade': comment.grade,
                'time': comment.time,
                'keyword': comment.keyword,
                'picturecount': comment_pictures.count(),
                'pictures': picture_data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '店铺不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class RecommendedShop(APIView):
    @staticmethod
    def get(request):
        # 获取用户的area_id
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        phone = decoded_token.get('phone')
        user = myUser.objects.get(mobile=phone)
        area_id = user.area_id
        preferences = UserPreference.objects.filter(user_id=user.id).values_list('category_id', flat=True)

        shop_list = Shop.objects.all()

        # 计算每个商店的推荐分数
        shop_scores = []
        for shop in shop_list:
            score = 0
            if shop.category_id in preferences:
                score += 5
            if shop.area_id == area_id:
                score += 5
            shop_scores.append((shop, score))

        random.shuffle(shop_scores)
        # 按照推荐分数从高到低排序
        shop_scores.sort(key=lambda x: x[1], reverse=True)
        # 选取推荐分数最高的10个商店
        recommended_shops = [shop for shop, score in shop_scores[:10]]

        # 将推荐结果转换为json格式的数据
        data = {
            'shopcount': len(recommended_shops),
            'recommended_shops': []
        }
        for shop in recommended_shops:
            data['recommended_shops'].append({
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

        # 返回json格式的数据
        return Response(data, status=status.HTTP_200_OK)


class PopularShop(APIView):
    @staticmethod
    def get(request):
        # 查询所有shop列表，并按照评分从高到低和评论数量从多到少排序
        shop_list = Shop.objects.all().order_by('grade', 'comments')

        # 如果shop数量大于等于20，则选取前20个shop作为候选结果
        if shop_list.count() >= 20:
            candidate_shops = list(shop_list)[:20]

        # 如果shop数量小于20，则选取所有shop作为候选结果
        else:
            candidate_shops = list(shop_list)

        # 在候选结果中随机选取5个shop作为推荐结果
        popular_shops = random.sample(candidate_shops, 5)

        # 将推荐结果转换为json格式的数据
        data = {
            'shopcount': 5,
            'popular_shops': []
        }
        for shop in popular_shops:
            data['popular_shops'].append({
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

        # 返回json格式的数据
        return Response(data, status=status.HTTP_200_OK)
