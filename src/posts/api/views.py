from django.db.models import Q
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView,
	)
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
from rest_framework.filters import  (
	SearchFilter,
	OrderingFilter,
)

from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
)

from posts.models import Post
from rest_framework import filters
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination
from .serializers import (
	PostListSerializer,
	PostDetailSerializer,
	PostCreateUpdateSerializer
	)


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter]
	search_fields = ['title', 'content', "user__first_name"]
	pagination_class = PostLimitOffsetPagination

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
