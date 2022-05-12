from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.movie_db.constans import OMDB_API_URL
from apps.movie_db.models import Movie, Comment
from apps.movie_db.omdb import OMDB
from apps.movie_db.serializers import MovieSerializer, CommentSerializer

from django.conf import settings


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-created_at')
    serializer_class = MovieSerializer
    omdb = OMDB(OMDB_API_URL, settings.OMDB_API_KEY)

    def create(self, request, *args, **kwargs):
        description = self.omdb.retrieve_description(request.data['title'])
        serializer = self.get_serializer(
            data={
                'title': request.data['title'],
                'description': description
            })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset
