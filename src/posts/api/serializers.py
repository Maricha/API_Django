from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post


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
	user = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'user',
			'url',
			'title',
			'slug',
			'content',
		]
	def get_user(self, obj):
		return str(obj.user.username)

class PostDetailSerializer(serializers.ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()
	image = SerializerMethodField()
	html = SerializerMethodField()
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
		]

	def get_html(self, obj):
		return obj.get_markdown()

	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image
