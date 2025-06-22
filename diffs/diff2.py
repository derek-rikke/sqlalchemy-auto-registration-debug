from sqlalchemy import Column, Integer, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.mapper import Mapper

from sqlalchemy_mptt.events import mptt_before_insert, mptt_before_update, mptt_before_delete

class BaseNestedSets:
    @classmethod
    def register_tree(cls):
        event.listen(cls, "before_insert", mptt_before_insert)
        event.listen(cls, "before_update", mptt_before_update)
        event.listen(cls, "before_delete", mptt_before_delete)

@event.listens_for(Mapper, "mapper_configured")
def auto_register(mapper, cls):
    if issubclass(cls, BaseNestedSets) and cls is not BaseNestedSets:
        cls.register_tree()

# Minimal schema
BaseNestedSets.id = declared_attr(lambda cls: Column(Integer, primary_key=True))
BaseNestedSets.left = declared_attr(lambda cls: Column("lft", Integer))
BaseNestedSets.right = declared_attr(lambda cls: Column("rgt", Integer))
