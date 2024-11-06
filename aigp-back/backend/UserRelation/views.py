from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Follow
from .serializers import UserRelationSerializer
from CustomUser.models import CUser
from UserInfo.models import UInfo

class FollowingView(APIView):
    authentication_classes = [JWTAuthentication]  # 添加 JWT 身份验证
    permission_classes = [IsAuthenticated]  # 添加权限类，确保用户已经通过身份验证

    def post(self, request):
        try:
            user_id = request.data.get('target_id')
            user = CUser.objects.get(id=user_id)

            token = request.auth
            
            my_user_id = token.payload.get('user_id')
            my_user = CUser.objects.get(id=my_user_id)

            uinfo = UInfo.objects.get(username=user.username)

            follow = Follow.objects.get(followed=user.username, follower=my_user.username)
            
            if follow:
                follow.delete()
                uinfo.followerCount -= 1
                uinfo.save()
            return Response({"result": "success"}, status=status.HTTP_200_OK)

        except CUser.DoesNotExist:
            return Response({"result": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        except UInfo.DoesNotExist:
            return Response({"result": "信息不存在"}, status=status.HTTP_404_NOT_FOUND)

        except Follow.DoesNotExist:
            serializer = UserRelationSerializer(data={"followed": user.username, "follower": my_user.username})
            if serializer.is_valid():
                serializer.save()
                uinfo.followerCount += 1
                uinfo.save()
            return Response({"result": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": "未知错误"}, status=status.HTTP_400_BAD_REQUEST)

