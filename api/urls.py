from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .email_auth import get_code, get_token
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UsersViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='title_reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review_comments'
)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

TOKEN_URLS = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

AUTH_URLS = [
    path('email/', get_code, name='get_conf_code'),
    path('token/', get_token, name='get_token_code'),
]

urlpatterns = [
    path('v1/token/', include(TOKEN_URLS)),
    path('v1/auth/', include(AUTH_URLS)),
    path('v1/', include(v1_router.urls)),
]
