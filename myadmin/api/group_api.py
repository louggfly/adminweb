from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from adminProject import settings
from myadmin.models import myUser, Group


class UserGroup(APIView):
    @staticmethod
    def get(request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        print(token)
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            groups = Group.objects.filter(status=1)
            groups = groups.filter(leader_id=user.id)
            data = {
                'groupcount': groups.count(),
                'groups': []
            }
            for group in groups:
                data['groups'].append({
                    'id': group.id,
                    'name': group.name,
                    'shop_id': group.shop_id,
                    'leader_id': group.leader_id,
                    'reserve_at': group.reserve_at,
                })
            return Response(data, status=status.HTTP_200_OK)
        except myUser.DoesNotExist:
            return Response({'status': 'failed', 'message': '无效的token'}, status=status.HTTP_400_BAD_REQUEST)


class CreateGroup(APIView):
    @staticmethod
    def post(request):
        try:
            name = request.data.get('name')
            shopId = request.data.get('shopId')
            leaderId = request.data.get('leaderId')
            reserve_at = request.data.get('reserve_at')
            ob = Group()
            ob.name = name
            ob.shop_id = shopId
            ob.leader_id = leaderId
            ob.time = datetime.now() + timedelta(hours=8)
            ob.reserve_at = datetime.strptime(reserve_at, "%Y-%m-%d %H:%M") + timedelta(hours=8)
            ob.save()
            return Response({'groupId': ob.id}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGroup(APIView):
    @staticmethod
    def post(request):
        try:
            id = request.data.get('groupId')
            name = request.data.get('name')
            shopId = request.data.get('shopId')
            leaderId = request.data.get('leaderId')
            reserve_at = request.data.get('reserve_at')
            group = Group.objects.get(id=id)
            group.name = name
            group.shop_id = shopId
            group.leader_id = leaderId
            group.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            group.reserve_at = datetime.strptime(reserve_at, "%Y-%m-%d %H:%M") + timedelta(hours=8)
            group.save()
            return Response(status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteGroup(APIView):
    @staticmethod
    def post(request):
        try:
            id = request.data.get('groupId')
            group = Group.objects.get(id=id)
            group.status = 9
            group.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            group.delete()
            return Response(status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)
