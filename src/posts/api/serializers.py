from rest_framework import serializers
from posts.models import Post


class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]

class PostListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'slug',
			'content',
		]

class PostDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'slug',
			'content',
			'publish'
		]
