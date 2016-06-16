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
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from comments.models import Comment
from rest_framework import filters
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination
from .serializers import (
	CommentSerializer,
	CommentChildSerializer,
	CommentDetailSerializer,
	create_comment_serializer,

	)


class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	permission_classes = [IsAuthenticated,]

	def get_serializer_class(self):
		model_type = self.request.GET.get("type")
		slug = self.request.GET.get("slug")
		parent_id = self.request.GET.get("parent_id", None)
		return create_comment_serializer(
			model_type=model_type,
			slug=slug,
			parent_id=parent_id,
			user=self.request.user
		)

class CommentDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(sefl, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


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
