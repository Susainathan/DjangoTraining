from django.urls import path
from .views import posts, votes

app_name = "posts"

urlpatterns = [
    path('listposts/', posts.PostListViewAPI.as_view()),
    path('createpost/', posts.PostCreateViewAPI.as_view()),
    path('post/<int:pk>', posts.DetailAPIVIew.as_view()),

    #Vote
    path('vote/', votes.ListVoteAPIView.as_view()),
    path('vote/<int:pk>/create', votes.VoteCreateAPIView.as_view()),
    path('vote/<int:pk>', votes.DetailAPIView.as_view())
]
