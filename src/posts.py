import re
from datetime import datetime, timedelta


class Posts:
    def __init__(self, id_, slug, title, created_at, owner_username):
        self.id_ = id_
        self.slug = slug
        self.title = title
        self.created_at = created_at
        self.owner_username = owner_username

    def contains_keywords(self, keywords):
        for keyword in keywords:
            pattern = rf"\b{keyword}\b"
            if re.search(pattern.lower(), self.title.lower()):
                return True
        return False

    def is_created_yesterday(self):
        today = datetime.now().date()
        post_date = datetime.strptime(self.created_at, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        yesterday = today - timedelta(days=1)
        return post_date == yesterday

    @staticmethod
    def extract_post_info(posts):
        post_info = {}
        for posts_data in posts:
            post = Posts(posts_data['id'], posts_data['slug'], posts_data['title'], posts_data['created_at'], posts_data['owner_username'])
            post_info[post.id_] = post
        return post_info
