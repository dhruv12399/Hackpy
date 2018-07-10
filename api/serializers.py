from rest_framework import serializers
from hackernews.models import Link, Comments

class LinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Link
		fields = ('id', 'title', 'url', 'parent')
		
class CommentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comments
		fields = ('id', 'content', 'linked_to', 'added_by', 'parent')
		