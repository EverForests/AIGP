from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from CustomUser.models import CUser
from .models import ImgInfo
from .serializers import ImgInfoSerializer

import cv2
from segment_anything import sam_model_registry, SamPredictor
import numpy as np
import os
import base64
from PIL import Image
from io import BytesIO

        
class ImgManageView(APIView):
    authentication_classes = [JWTAuthentication]  # 添加 JWT 身份验证
    permission_classes = [IsAuthenticated]  # 添加权限类，确保用户已经通过身份验证

    # postimg
    def post(self, request):
        try:
            serializer = ImgInfoSerializer(data=request.data)
            if serializer.is_valid():
                newimg = serializer.save()
                newimg.image.name = newimg.image.name.replace('images/', '/static/')
                new_serializer = ImgInfoSerializer(newimg)
                response_data = {
                    "result": "success",
                    **new_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"result": "提交信息不全"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': "图片上传失败"})

    # get imglist
    def get(self, request):
        try:
            user_id = request.query_params['user_id']
            user = CUser.objects.get(id=user_id)
            imglist = ImgInfo.objects.filter(username=user.username, flag=True)
            for img in imglist:
                img.image.name = img.image.name.replace('images/', '/static/')
            serializer = ImgInfoSerializer(imglist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CUser.DoesNotExist:
            return Response({"result": "User does not exist for the given user_id."}, status=status.HTTP_404_NOT_FOUND)
        except ImgInfo.DoesNotExist:
            return Response({"result": "ImgInfo does not exist for the given username."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # delete img
    def delete(self, request):
        try:
            image_id = request.data.get('post_id')
            image = ImgInfo.objects.get(id=image_id)
            image.delete()
            os.remove(image.image.name)  # 回收资源
            return Response({"result": "success"}, status=status.HTTP_200_OK)
        except image.DoesNotExist:
            return Response({"result": "Image does not exist for the given ID."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class imgEmbeddingCreateView(APIView):
    def post(self, request):
        try:
            img_id = request.data.get('img_id')
            img = ImgInfo.objects.get(id=img_id)
            # 生成掩膜
            checkpoint = "embeddings/sam_vit_h_4b8939.pth"
            model_type = "vit_h"
            sam = sam_model_registry[model_type](checkpoint=checkpoint)
            sam.to(device='cpu')
            predictor = SamPredictor(sam)

            image = cv2.imread(img.image.name)
            predictor.set_image(image)
            image_embedding = predictor.get_image_embedding().cpu().numpy()
            npy_file_path = "embeddings/" + img.title + "_embedding.npy"
            np.save(npy_file_path, image_embedding)
            type(image_embedding),image_embedding.shape

            # 加载.npy文件
            np_array = np.load(npy_file_path)
            # 将.npy文件数据转换为JSON格式
            npy_data = {
                "data": np_array.tolist(),  # 将numpy数组转换为Python列表
                "shape": np_array.shape,     # 获取数组形状
                "dType": str(np_array.dtype) # 获取数组数据类型并转换为字符串
            }

            response_data = {
                "result": "success",
                **npy_data
            }

            os.remove(npy_file_path)  # 回收资源
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ImgInfo.DoesNotExist:
            return Response({"result": "Image does not exist for the given ID."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SocialImgListShow(APIView):
    def get(self, request):
        try:
            imglist = ImgInfo.objects.filter(flag=True)
            for img in imglist:
                img.image.name = img.image.name.replace('images/', '/static/')
            serializer = ImgInfoSerializer(imglist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ImgInfo.DoesNotExist:
            return Response({"result": "ImgInfo does not exist for the given username."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)