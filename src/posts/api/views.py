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

from posts.models import Post
from rest_framework import filters
from .permissions import IsOwnerOrReadOnly
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

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all()
		title = self.request.query_params.get('abc', None)

		if title is not None:
			queryset_list = queryset_list.filter(title="Cos")
		#query = self.request.GET.get("a")
		return queryset_list


		#if query:
			#queryset_list = Post.objects.filter(title="Cos")
			#queryset_list = queryset_list.filter(title="Cos")
				#Q(title__icontains=query)|
				#Q(content__icontains=query)
				#).distinct()
		#return queryset_list


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