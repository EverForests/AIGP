from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

from CustomUser.models import CUser
from UserInfo.models import UInfo
from UserRelation.models import Follow

class UserGetInfoView(APIView):
    # 开启jwt验证
    authentication_classes = [JWTAuthentication]  # 添加 JWT 身份验证
    permission_classes = [IsAuthenticated]  # 添加权限类，确保用户已经通过身份验证

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            print(user_id)
            user = CUser.objects.get(id=user_id)
            print(123)
            info = UInfo.objects.get(username=user.username)
            
            token = request.auth
            myid = token.payload.get('user_id')
            print(myid)
            myuser = CUser.objects.get(id=myid)
            follow = Follow.objects.filter(followed=user.username, follower=myuser.username)

            is_followed = False
            if follow:
                is_followed = True

            photo = info.photo
            followerCount = info.followerCount
            username = user.username

            return Response({
                "id": user_id,
                "username": username,
                "photo": photo.name.replace('images/', '/static/'),
                "followerCount": followerCount,
                "is_followed": is_followed
            }, status=status.HTTP_200_OK)
        except CUser.DoesNotExist:
            return Response({"result": "User does not exist for the given user_id."}, status=status.HTTP_404_NOT_FOUND)
        except UInfo.DoesNotExist:
            return Response({"result": "UInfo does not exist for the given username."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": "登录异常", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        