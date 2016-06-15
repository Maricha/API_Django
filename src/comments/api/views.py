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

from comments.models import Comment
from rest_framework import filters
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination
from .serializers import (
	CommentSerializer,

	)


# class PostCreateAPIView(CreateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	permission_classes = [IsAuthenticated, IsAdminUser]
#
# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
	serializer_class = CommentSerializer
	filter_backends = [SearchFilter]
	search_fields = ['content', "user__first_name"]
	pagination_class = PostLimitOffsetPagination

	def get_queryset(self, *args, **kwargs):
		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list


# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	permission_classes = [IsOwnerOrReadOnly]
#
# 	def perform_update(self, serializer):
# 		serializer.save(user=self.request.user)

# class PostDeleteAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostListSerializer

class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
