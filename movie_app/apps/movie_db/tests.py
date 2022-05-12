from mock import patch

from rest_framework.test import APIClient, APITestCase


@patch('apps.movie_db.omdb.OMDB.retrieve_description',
       return_value='movie_description_in_json')
class MovieTest(APITestCase):
    client = APIClient()

    def test_post_movie(self, mock_retrieve_description):

        response = self.client.post('/movies/', data={
            'title': 'cat',
        })
        self.assertEqual(response.data['title'], 'cat')
        self.assertEquals(response.data['description'], 'movie_description_in_json')
        self.assertEqual(response.status_code, 201)

    def test_post_movie_no_title(self, mock_retrieve_description):
        response = self.client.post('/movies/', data={
            'title': '',
        })
        self.assertEqual(response.status_code, 400)

    def test_get_movies(self, mock_retrieve_description):
        # populating db
        self.client.post('/movies/', data={
            'title': 'cat',
        })
        self.client.post('/movies/', data={
            'title': 'django',
        })
        response = self.client.get('/movies/')
        self.assertEqual(len(response.data), 2)


@patch('apps.movie_db.omdb.OMDB.retrieve_description',
       return_value='movie_description_in_json')
class CommentTest(APITestCase):
    client = APIClient()

    def test_post_comment(self, mock_retrieve_description):
        self.client.post('/movies/', data={
            'title': 'cat',
        })
        response = self.client.post('/comments/', data={
            'movie': '1', 'comment_text': 'alamakota'
        })
        self.assertEqual(response.data['movie'], 1)
        self.assertEqual(response.data['comment_text'], 'alamakota')

    def test_get_comments(self, mock_retrieve_description):
        # populating db
        self.client.post('/movies/', data={
            'title': 'cat',
        })
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'alamakota'})
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'alamapsa'})
        response = self.client.get('/comments/')
        self.assertEqual(len(response.data), 2)

    def test_get_filtered_comments(self, mock_retrieve_description):
        self.client.post('/movies/', data={
            'title': 'cat',
        })
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'alamakota'})
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'alamapsa'})
        response = self.client.get('/comments/?movie_id=1')
        self.assertEqual(len(response.data), 2)
        for i in response.data:
            self.assertEqual(i['movie'], 1)
