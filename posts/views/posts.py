import django_filters

from django.http import Http404
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import permissions

from posts.serializers import PostSerializer
from posts.filters import PostFilter
from posts.models import Posts


@extend_schema(tags=['Post'], summary='list all post')
class PostListViewAPI(ListAPIView):
    """
    List all posts
    """
    serializer_class = PostSerializer
    filterset_class = PostFilter
    queryset = Posts.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema(tags=['Post'], summary='Create post')
class PostCreateViewAPI(CreateAPIView):
    """
    Create Post API
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class DetailAPIVIew(APIView):
    """
    Retrive, update, delete a post instance
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            raise Http404

    @extend_schema(tags=['Post'], summary='get one post')
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context = self.get_renderer_context())
        return Response(serializer.data)


    @extend_schema(tags=['Post'], summary='update post')
    def put(self,request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context=self.get_renderer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Post'], summary='Delete post')
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
