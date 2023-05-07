import re
from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from adminProject import settings
from myadmin.models import myUser, CommentPicture, Shop, UserFavourite, UserComment, UserPreference, ShopCategory


class AllCategory(APIView):
    @staticmethod
    def get(request):
        try:
            categories = ShopCategory.objects.filter(status=1)
            data = {
                'categorycount': categories.count(),
                'categories': []
            }
            for item in categories:
                data['categories'].append({
                    'id': item.id,
                    'name': item.name,
                })
            return Response(data, status=status.HTTP_200_OK)
        except ShopCategory.DoesNotExist:
            return Response({'status': 'failed', 'message': '种类列表不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceList(APIView):
    @staticmethod
    def get(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            userPreference = UserPreference.objects.filter(user_id=user.id)
            userPreference = userPreference.filter(status=1)
            categories = ShopCategory.objects.filter(status=1)
            data = {
                'preferencecount': userPreference.count(),
                'preferences': []
            }
            for item in userPreference:
                preference = categories.get(id=item.category_id)
                data['preferences'].append({
                    'id': item.id,
                    'name': item.name,
                })
            return Response(data, status=status.HTTP_200_OK)
        except UserPreference.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户偏好不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceCreate(APIView):
    @staticmethod
    def post(request):
        try:
            categoryId = request.data.get("categoryId")
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            ob = UserPreference()
            ob.user_id = user.id
            ob.category_id = categoryId
            ob.status = 1
            ob.save()
            return Response(status=status.HTTP_200_OK)
        except UserPreference.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户偏好不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceDelete(APIView):
    @staticmethod
    def post(request):
        try:
            categoryId = request.data.get("categoryId")
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            userPreference = UserPreference.objects.filter(user_id=user.id)
            userPreference = userPreference.get(category_id=categoryId)
            userPreference.delete()
            return Response(status=status.HTTP_200_OK)
        except UserPreference.DoesNotExist:
            return Response({'status': 'failed', 'message': '用户偏好不存在！'}, status=status.HTTP_400_BAD_REQUEST)
