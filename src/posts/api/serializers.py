from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post
from comments.api.serializers import CommentListSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

post_detail_url = HyperlinkedIdentityField (
	view_name="posts-api:detail",
	lookup_field='pk'
)
class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]

class PostListSerializer(serializers.ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Post
		fields = [
			'user',
			'url',
			'title',
			'slug',
			'content',
		]

class PostDetailSerializer(serializers.ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'id',
			'user',
			'title',
			'slug',
			'content',
			'publish',
			'url',
			'image',
			'html',
			'comments',
		]

	def get_html(self, obj):
		return obj.get_markdown()

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self, obj):
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentListSerializer(c_qs, many=True).data
		return comments
