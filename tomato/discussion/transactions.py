# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError

from tomato.discussion.core import db
from tomato.discussion.core import jsonrpc
from tomato.discussion.models import Topic
from tomato.discussion.models import TopicMember
from tomato.discussion.models import Discussion
from tomato.discussion.models import Comment

@jsonrpc.method('tomato.discussion.get_topic')
def get_topic(topic_id):
    topic = Topic.query.get(topic_id)
    return topic and topic.to_dict()

@jsonrpc.method('tomato.discussion.add_topic')
def add_topic():
    topic = Topic()
    db.session.add(topic)
    db.session.commit()
    return topic.id

@jsonrpc.method('tomato.discussion.add_member_to_topic')
def add_member_to_topic(user_id, topic_id):
    try:
        member = TopicMember(user_id=user_id, topic_id=topic_id)
        topic = Topic.query.get(topic_id)
        topic.members_count = Topic.members_count + 1
        db.session.add(topic)
        db.session.commit()
        return member.to_dict()
    except IntegrityError:
        db.session.rollback()
        member = TopicMember.query.filter_by(
            user_id=user_id, topic_id=topic_id,
        ).first()
        member.is_deleted = False
        db.session.add(member)
        topic = Topic.query.get(topic_id)
        topic.members_count = Topic.members_count + 1
        db.session.add(topic)
        db.session.commit()
        return member.to_dict()
    except:
        db.session.rollback()
        raise

@jsonrpc.method('tomato.discussion.remove_member_from_topic')
def remove_member_from_topic(user_id, topic_id):
    member = TopicMember.query.filter_by(
        user_id=user_id, topic_id=topic_id
    ).first()
    if not member:
        return False
    if member.is_deleted:
        return True
    member.is_deleted = True
    member.is_admin = False
    topic = Topic.query.get(topic_id)
    topic.members_count = Topic.members_count - 1
    db.session.add(member)
    db.session.add(topic)
    db.session.commit()
    return True

@jsonrpc.method('tomato.discussion.grant_topic_member_as_admin')
def grant_topic_member_as_admin(user_id, topic_id):
    member = TopicMember.query.filter_by(
        user_id=user_id, topic_id=topic_id
    ).first()
    if not member:
        return False
    member.is_admin = True
    db.session.add(member)
    db.session.commit()
    return True

@jsonrpc.method('tomato.discussion.revoke_topic_member_as_admin')
def revoke_topic_member_as_admin(user_id, topic_id):
    member = TopicMember.query.filter_by(
        user_id=user_id, topic_id=topic_id
    ).first()
    if not member:
        return False
    member.is_admin = False
    db.session.add(member)
    db.session.commit()
    return True

@jsonrpc.method('tomato.discussion.get_topic_admin_members')
def get_topic_admin_members(topic_id):
    members = TopicMember.query.filter_by(
        topic_id=topic_id,
        is_admin=True,
    ).all()
    return [member.to_dict() for member in members]

@jsonrpc.method('tomato.discussion.get_topic_non_admin_members')
def get_topic_non_admin_members(topic_id, offset=0, limit=20):
    members = TopicMember.query.filter_by(
        topic_id=topic_id,
        is_admin=False,
    ).offset(offset).limit(limit).all()
    return [member.to_dict() for member in members]

@jsonrpc.method('tomato.discussion.add_topic_discussion')
def add_topic_discussion(topic_id, user_id, title, content):
    discussion = Discussion(
        topic_id=topic_id,
        user_id=user_id,
        title=title,
        content=content,
    )
    db.session.add(discussion)
    topic = Topic.query.get(topic_id)
    topic.discussions_count = Topic.discussions_count + 1
    db.session.add(topic)
    db.session.commit()
    return discussion.id

@jsonrpc.method('tomato.discussion.get_discussion')
def get_discussion(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    return discussion and discussion.to_dict()

@jsonrpc.method('tomato.discussion.delete_discussion')
def delete_discussion(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if not discussion:
        return False
    discussion.is_deleted = True
    db.session.add(discussion)
    db.session.commit()

@jsonrpc.method('tomato.discussion.update_discussion')
def update_discussion(discussion_id, title, content):
    discussion = Discussion.query.get(discussion_id)
    if not discussion:
        return False
    discussion.title = title
    discussion.content = content
    db.session.add(discussion)
    db.session.commit()
    return True

@jsonrpc.method('tomato.discussion.get_topic_discussions')
def get_topic_discussions(topic_id, offset=0, limit=20):
    discussions = Discussion.query.filter_by(
        topic_id=topic_id, is_deleted=False
    ).offset(offset).limit(limit)
    return [discussion.to_dict() for discussion in discussions]

@jsonrpc.method('tomato.discussion.get_user_published_discussions')
def get_user_published_discussions(user_id, offset=0, limit=20):
    discussions = Discussion.query.filter_by(
        user_id=user_id, is_deleted=False
    ).offset(offset).limit(limit)
    return [discussion.to_dict() for discussion in discussions]

@jsonrpc.method('tomato.discussion.add_discussion_comment')
def add_discussion_comment(discussion_id, user_id, content):
    comment = Comment(
        discussion_id=discussion_id,
        user_id=user_id,
        content=content,
    )
    db.session.add(comment)
    discussion = Discussion.query.get(discussion_id)
    discussion.comments_count = Discussion.comments_count + 1
    db.session.add(discussion)
    db.session.commit()
    return comment.to_dict()

@jsonrpc.method('tomato.discussion.delete_discussion_comment')
def delete_discussion_comment(discussion_comment_id):
    comment = Discussion.query.get(discussion_comment_id)
    if comment.is_deleted:
        return False
    comment.is_deleted = True
    discussion = Discussion.query.get(comment.discussion_id)
    discussion.comments_count = Discussion.comments_count - 1
    db.session.add(comment)
    db.session.add(discussion)
    db.session.commit()
    return True

@jsonrpc.method('tomato.discussion.get_discussion_comments')
def get_discussion_comments(discussion_id, offset=0, limit=20):
    comments = Comment.query.filter_by(
        discussion_id=discussion_id, is_deleted=False
    ).offset(offset).limit(limit).all()
    return [comment.to_dict() for comment in comments]
