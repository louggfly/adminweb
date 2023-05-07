from datetime import datetime

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from adminProject import settings
from myadmin.models import UserComment, CommentPicture, myUser


class AllComment(APIView):
    @staticmethod
    def get(request):
        try:
            comments = UserComment.objects.filter(status=1)
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
            return Response({'status': 'failed', 'message': '评论不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class SearchComment(APIView):
    @staticmethod
    def post(request):
        try:
            keyword = request.data.get('keyword')
            comments = UserComment.objects.filter(content__contains=keyword)
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
        except:
            return Response({'status': 'failed', 'message': '评论不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class ReleaseComment(APIView):
    @staticmethod
    def post(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            phone = decoded_token.get('phone')
            user = myUser.objects.get(mobile=phone)
            shopId = request.data.get('shopId')
            comment = request.data.get('comment')
            grade = request.data.get('grade')
            imageUrl = request.data.get('imageUrl')
            ob = UserComment()
            ob.user_id = user.id
            ob.content = comment
            ob.shop_id = shopId
            ob.status = 1
            ob.keyword = ""
            ob.grade = grade
            ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            ob.save()
            if len(imageUrl) != 0:
                for item in imageUrl:
                    pob = CommentPicture()
                    pob.picture_link = item
                    pob.comment_id = ob.id
                    pob.status = 1
                    pob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    pob.save()
            return Response({'commentId': ob.id}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateComment(APIView):
    @staticmethod
    def post(request):
        try:
            id = request.data.get('commentId')
            shopId = request.data.get('shopId')
            comment = request.data.get('comment')
            grade = request.data.get('grade')
            imageUrl = request.data.get('imageUrl')
            ob = UserComment.objects.get(id=id)
            ob.content = comment
            ob.shop_id = shopId
            ob.status = 1
            ob.keyword = ""
            ob.grade = grade
            ob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            ob.save()
            if len(imageUrl) != 0:
                oldPictures = CommentPicture.objects.filter(comment_id=ob.id)
                for item in oldPictures:
                    item.status = 9
                    item.time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    item.delete()
                for item in imageUrl:
                    pob = CommentPicture()
                    pob.picture_link = item
                    pob.comment_id = ob.id
                    pob.status = 1
                    pob.time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    pob.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteComment(APIView):
    @staticmethod
    def post(request):
        try:
            id = request.data.get('commentId')
            comment = UserComment.objects.get(id=id)
            comment.status = 9
            comment.time = datetime.now().strftime("%Y-%m-%d %H:%M")
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'status': 'failed', 'message': '未知错误'}, status=status.HTTP_400_BAD_REQUEST)
