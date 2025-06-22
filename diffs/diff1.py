from sqlalchemy import Column, Integer, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from sqlalchemy_mptt.events import mptt_before_insert, mptt_before_update, mptt_before_delete

class BaseNestedSets:
    @classmethod
    def __declare_first__(cls):
        cls.__mapper__.batch = False
        if cls is not BaseNestedSets:
            @event.listens_for(cls, "after_configured", once=True)
            def register():
                cls.register_tree()

    @classmethod
    def register_tree(cls):
        event.listen(cls, "before_insert", mptt_before_insert)
        event.listen(cls, "before_update", mptt_before_update)
        event.listen(cls, "before_delete", mptt_before_delete)

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def left(cls):
        return Column("lft", Integer)

    @declared_attr
    def right(cls):
        return Column("rgt", Integer)
