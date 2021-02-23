export DB_HOST='localhost:5432'
export FLASK_APP='api.py'
export FLASK_ENV='development'
export DB_PATH='postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
export AUTH0_DOMAIN='coffeeprojectudacity.us.auth0.com'
export ALGORITHMS=["RS256"]