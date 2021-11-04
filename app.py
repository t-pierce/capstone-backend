from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    content = db.Column(db.String, nullable=False, unique=False)
    image = db.Column(db.String, nullable=True, unique=False)

    def __init__(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image

class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content", "image")

blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)

@app.route("/blog_post/add", methods=["POST"])
def add_blog_post():
    title = request.json.get("title")
    content = request.json.get("content")
    image = request.json.get("image")

    new_blog = BlogPost(title, content, image)
    db.session.add(new_blog)
    db.session.commit()

    return jsonify(blog_post_schema.dump(new_blog))

@app.route("/blog_post/get", methods=["GET"])
def get_all_blog_posts():
    all_blog_posts = BlogPost.query.all()
    return jsonify(blog_posts_schema.dump(all_blog_posts))

if __name__ == "__main__":
    app.run(debug=True)
