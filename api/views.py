import logging

from django.contrib.auth import get_user_model
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (filters, mixins, permissions,
                            status, viewsets)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from titles.models import Category, Genre, Review, Title

from .custom_paginations import StandardResultsSetPagination
from .filters import TitlesFilter
from .permissions import (AuthorOrManageSiteRolesPermission, IsAdminPermission,
                          IsSuperUserOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MeSerializer, ReviewSerializer,
                          ReviewUpdateSerializer, TitleCreateSerializer,
                          TitleListSerializer, UserSerializer)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

User = get_user_model()


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin):
    """A viewset for category model with default actions
       inherited from viewsets.GenericViewSet."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsSuperUserOrReadOnlyPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    search_fields = ['=name']


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin):
    """A viewset for genre model with default actions
       inherited from viewsets.GenericViewSet."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsSuperUserOrReadOnlyPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ('name',)
    filterset_fields = ('slug',)
    lookup_field = 'slug'
    search_fields = ['=name']


class TitleViewSet(viewsets.ModelViewSet):
    """A viewset for title model with default actions
       inherited from viewsets.ModelViewSet."""
    queryset = (Title.objects
                     .annotate(rating=Avg('reviews__score'))
                     .order_by('-year'))
    permission_classes = [IsSuperUserOrReadOnlyPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ('name', 'year', 'category', 'genre', )
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """A viewset for user model with default actions
       inherited from viewsets.ModelViewSet."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminPermission,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False,
            methods=['patch', 'GET'],
            permission_classes=[permissions.IsAuthenticated],
            )
    def me(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(pk=request.user.pk).first()
            if request.method == 'GET':
                user_serializer = MeSerializer(user)
                return Response(
                    user_serializer.data, status=status.HTTP_200_OK
                )

            if request.method == 'PATCH':
                user_serializer = MeSerializer(
                    user,
                    data=request.data,
                    partial=True
                )
                if user_serializer.is_valid(raise_exception=True):
                    user = user_serializer.save()
                    return Response(
                        user_serializer.data,
                        status=status.HTTP_200_OK
                    )
                return Response(
                    user_serializer.data,
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            'Unauthorized user', status=status.HTTP_401_UNAUTHORIZED
        )


class ReviewsViewSet(viewsets.ModelViewSet):
    """A viewset for review model with default actions
       inherited from viewsets.ModelViewSet."""
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrManageSiteRolesPermission,
    ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title_id', ]
    lookup_fields = ['title_id', 'review_id', ]

    def get_serializer_class(self):
        logging.debug(
            f'ReviewsViewSet. get_serializer_class. Action - {self.action}'
        )
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        logging.debug(f'ReviewsViewSet, get_queryset. Title - {title}')
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """A viewset for comment model with default actions
       inherited from viewsets.ModelViewSet."""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrManageSiteRolesPermission,
    ]
    pagination_class = StandardResultsSetPagination
    lookup_fields = ['title_id', 'review_id', 'comment_id', ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review, id=review_id, title__id=title_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review, id=review_id, title__id=title_id
        )
        serializer.save(author=self.request.user, review=review)
