import datetime

from src.domain.comments import Comment

comments = [
    Comment(
        blog_id='blog_id_1',
        content='Great post!',
        author='User1',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True),
    Comment(
        blog_id='blog_id_2',
        content='Nice article!',
        author='User2',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True),
]
