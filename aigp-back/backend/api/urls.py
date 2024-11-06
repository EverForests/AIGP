# urls.py

from django.urls import path, re_path
from blog.views import ArticleList, ArticleDetail
from rest_framework.urlpatterns import format_suffix_patterns
from CustomUser.views import TokenObtainView, TokenRefreshView, UserRegisterView, UserIdSearchView
from UserInfo.views import UserGetInfoView
from ImgSrc.views import ImgManageView, imgEmbeddingCreateView, SocialImgListShow
from UserRelation.views import FollowingView

urlpatterns = [
    re_path(r'^articles/$', ArticleList.as_view()),
    re_path(r'^articles/(?P<pk>[0-9]+)$', ArticleDetail.as_view()),

    path('token/', TokenObtainView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('searchuserid/', UserIdSearchView.as_view()),

    path('register/', UserRegisterView.as_view()),
    path('getinfo/', UserGetInfoView.as_view()),

    path('postimg/', ImgManageView.as_view()),
    path('getimglist/', ImgManageView.as_view()),
    path('deleteimg/', ImgManageView.as_view()),
    path('embedding/', imgEmbeddingCreateView.as_view()),
    path('socialimg/', SocialImgListShow.as_view()),

    path('follow/', FollowingView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

