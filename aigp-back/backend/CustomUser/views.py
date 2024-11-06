from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.hashers import check_password

from .models import CUser
from UserInfo.models import UInfo
from .serializers import UserSerializer
from UserInfo.serializers import UserInfoSerializer

def authenticate(username=None, password=None):
    try:
        user = CUser.objects.get(username=username)
        if password == user.password:
            return user
    except CUser.DoesNotExist:
        pass
    return None

class TokenObtainView(APIView):
    def post(self, request, format=None):
        # 根据用户提供的凭据验证用户身份
        # 如果验证通过，生成访问令牌和刷新令牌
        username = request.data['username']
        password = request.data['password']
        
        if username and password is None:
            return Response({'error': '用户名或密码为空'})

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)  # RefreshToken生成令牌
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh = request.data['refresh']
            if refresh:
                token = RefreshToken(refresh)
                access = str(token.access_token)
                return Response({'access': access})
            else:
                return Response({'error': 'Refresh token is missing.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
class UserRegisterView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            password_confirm = request.data['password_confirm']
            
            if not all([username, password, password_confirm]):
                return Response({'result': '用户名或密码不能为空'})
            
            elif password != password_confirm:
                return Response({'result': '两次输入的密码不一致'})

            elif CUser.objects.get(username=username):
                return Response({'result': '用户名已存在'})

            else:
                return Response({'result': '未知错误'})
        
        # 一定要捕获异常
        except CUser.DoesNotExist:
            # 保存 UserSerializer
            userserializer = UserSerializer(data=request.data)
            if userserializer.is_valid():
                userserializer.save()

                # 保存 InfoSerializer
                userinfoserializer = UserInfoSerializer(data={"username": username})
                if userinfoserializer.is_valid():
                    userinfoserializer.save()
                    return Response({'result': 'success'})
                else:
                    # 如果 InfoSerializer 保存失败，需要删除已经创建的用户
                    print(userinfoserializer.errors)
                    userserializer.instance.delete()
                    return Response({'result': '验证失败'})
            return Response({'result': '验证失败'})
        
class UserIdSearchView(APIView):
    def get(self, request):
        try:
            username = request.query_params.get('username')
            user = CUser.objects.get(username=username)

            return Response({
                "id": user.id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": "登录异常", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
