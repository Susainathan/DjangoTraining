from rest_framework import serializers
from .models import Posts, Vote


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'votes']
        read_only_fields = ['created']

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'voter', 'post']
