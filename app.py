import os
from functools import wraps

from flask import Flask, request, jsonify, make_response, render_template, abort
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, desc
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'article.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(120))
    author = db.Column(db.String(120))
    votes = db.Column(db.Integer)

    def __init__(self, title, content, author, votes=0):
        self.title = title
        self.content = content
        self.author = author
        self.votes = votes


class ArticleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'content', 'author', 'votes')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/")
def main():
    return render_template('article.html')


def validate_json(*expected_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_object = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    abort(400)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# endpoint to create new article
@app.route("/create_article", methods=["POST"])
@validate_json('title', 'author', 'content')
def add_article():
    try:
        json_object = request.get_json()
        title = json_object['title']
        author = json_object['author']
        content = json_object['content']
        new_article = Article(title, author, content)
        db.session.add(new_article)
        db.session.commit()
        return jsonify(new_article.id)
    except exc.SQLAlchemyError:
        return make_response("Data Error", 400)
    except IntegrityError:
        return make_response("", 409)
    except (KeyError, TypeError):
        return make_response("", 400)


# endpoint to show all articles
@app.route("/list_articles", methods=["GET"])
def get_article():
    all_articles = Article.query.order_by(desc(Article.votes)).all()
    result = articles_schema.dump(all_articles)
    return jsonify(result)


# endpoint to update article
@app.route("/vote_article/<id>", methods=["PUT"])
def article_update(id):
    article = Article.query.get(id)
    article.votes = article.votes + 1
    db.session.commit()
    return article_schema.jsonify(article)


if __name__ == '__main__':
    app.run(debug=True)
