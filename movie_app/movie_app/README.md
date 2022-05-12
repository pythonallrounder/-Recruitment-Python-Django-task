### Solution

2. pip install -r requirements.txt

3. Generate your omdb api key from: http://www.omdbapi.com/apikey.aspx and export it in your console:

    export OMDB_API_KEY=[your_api_key]
    example
    run this command in your terminal in code dir
    #there should be your generated key or you can try with this also 
    set OMDB_API_KEY=a5b2811d 


4. Set up db:

    python manage.py makemigrations
    python manage.py migrate

5. Run your application locally:

    python manage.py runserver

6. Check your application on `127.0.0.1:8000`



- POST /movies/
Add movies to db requires only movie title. Description will be automatically fetched from OMDB.

- GET /movies/
Will show all movies in db ordered by data added descending.

- GET /comments/
Will show all comments in db ordered by data added descending.

- GET /comments/?movie_id=[your_movie_id]
Will show all comments associated movie with passed id.

- POST /comments/
Add comment to a movie by passing comment text and movie id to which you want to add a comment.
