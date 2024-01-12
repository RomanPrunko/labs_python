from flask import url_for
from flask_login import current_user
from app.authentication.models import User
from app.post.models import Post
from app import db



def test_get_all_posts(init_database):
    number_of_todos = Post.query.count()
    assert number_of_todos == 2


def test_delete_post(client, init_database):
    response = client.get(
        url_for('post.delete', id=1),
        follow_redirects=True
    )
    
    post = Post.query.filter_by(id=1).first()
    
    assert response.status_code == 200
    assert post is None
    assert b'Post has been deleted' in response.data
