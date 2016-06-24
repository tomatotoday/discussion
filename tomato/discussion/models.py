# -*- coding: utf-8 -*-

from time import mktime
from datetime import datetime

from tomato.discussion.core import db

class Topic(db.Model):

    __tablename__ = 'topic'

    id = db.Column(db.Integer(), primary_key=True)
    members_count = db.Column(db.Integer(), default=0, nullable=False)
    discussions_count = db.Column(db.Integer(), default=0, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            members_count=self.members_count,
            discussions_count=self.discussions_count,
            created_at=mktime(self.created_at.timetuple()),
        )

class TopicMember(db.Model):

    __tablename__ = 'topic_member'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'topic_id', name='ux_topic_member'),
        db.Index('ix_topic_member_admin', 'topic_id', 'is_admin'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            topic_id=self.topic_id,
            user_id=self.user_id,
            is_admin=self.is_admin,
            is_deleted=self.is_deleted,
            updated_at=mktime(self.updated_at.timetuple()),
            created_at=mktime(self.created_at.timetuple()),
        )

class Discussion(db.Model):

    __tablename__ = 'topic_discussion'

    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())
    comments_count = db.Column(db.Integer(), default=0, nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime())

    def to_dict(self):
        return dict(
            id=self.id,
            topic_id=self.topic_id,
            user_id=self.user_id,
            title=self.title,
            content=self.content,
            comments_count=self.comments_count,
            is_deleted=self.is_deleted,
            created_at=mktime(self.created_at.timetuple()),
        )

class Comment(db.Model):

    __tablename__ = 'topic_discussion_comment'

    id = db.Column(db.Integer(), primary_key=True)
    discussion_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Text())
    is_deleted = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime())

    def to_dict(self):
        return dict(
            id=self.id,
            discussion_id=self.discussion_id,
            user_id=self.user_id,
            title=self.title,
            content=self.content,
            is_deleted=self.is_deleted,
            created_at=mktime(self.created_at.timetuple()),
        )
