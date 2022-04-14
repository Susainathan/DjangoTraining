import django_filters
from django.http import Http404
from drf_spectacular.utils import extend_schema

from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import permissions

from posts.models import Vote, Posts
from posts.serializers import VoteSerializer, CreateVoteSerializer


@extend_schema(tags=['Votes'], summary='List all votes')
class ListVoteAPIView(ListAPIView):
    """
    List all votes instance
    """
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema(tags=['Votes'], summary='create votes')
class VoteCreateAPIView(CreateAPIView):
    """
    Create Vote instance
    """
    serializer_class = CreateVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Posts.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted !!!')
        serializer.save(voter=self.request.user, post=Posts.objects.get(pk=self.kwargs['pk']))


class DetailAPIView(APIView):
    """
    Retrive, update and delete instance
    """
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_objects(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            raise Http404

    @extend_schema(tags=['Votes'])
    def delete(self, request, pk):
        vote = self.get_objects(pk)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
