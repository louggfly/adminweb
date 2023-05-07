from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myadmin.models import Notice


class AllNotice(APIView):
    @staticmethod
    def get(request):
        notices = Notice.objects.filter(status=1)
        notice_data = []
        for notice in notices:
            notice_data.append({
                'id': notice.id,
                'admin_id': notice.admin_id,
                'title': notice.title,
                'content': notice.content,
            })
        data = {
            'noticecount': notices.count(),
            'notices': notice_data,
        }
        return Response(data, status=status.HTTP_200_OK)
