from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myadmin.models import Area


class AllArea(APIView):
    @staticmethod
    def get(request):
        try:
            areas = Area.objects.filter(status=1)
            data = {
                'areacount': areas.count(),
                'areas': []
            }
            for area in areas:
                data['areas'].append({
                    'id': area.id,
                    'name': area.name,
                })
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '地区不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class SearchArea(APIView):
    @staticmethod
    def post(request):
        try:
            keyword = request.data.get('keyword')
            areas = Area.objects.filter(status=1)
            areas = areas.filter(name__contains=keyword)
            data = {
                'areacount': areas.count(),
                'areas': []
            }
            for area in areas:
                data['areas'].append({
                    'id': area.id,
                    'name': area.name,
                })
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '地区不存在！'}, status=status.HTTP_400_BAD_REQUEST)
