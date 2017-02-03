#!flask/bin/python

"""Movie Recommender API"""

from app import app, oauth

if __name__ == '__main__':
    app.run(debug=True)
    oauth.init_app(app)
