from sqlalchemy import Column, event, ForeignKey, Index, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.session import Session

from sqlalchemy_mptt.events import mptt_before_delete, mptt_before_insert, mptt_before_update
from sqlalchemy_mptt.events import _get_tree_table

class BaseNestedSets(object):
    @declared_attr
    def __table_args__(cls):
        return (
            Index('%s_lft_idx' % cls.__tablename__, "lft"),
            Index('%s_rgt_idx' % cls.__tablename__, "rgt"),
            Index('%s_level_idx' % cls.__tablename__, "level"),
        )

    @classmethod
    def __declare_first__(cls):
        cls.__mapper__.batch = False  # no auto-registration logic here

    @classmethod
    def register_tree(cls):
        event.listen(cls, "before_insert", mptt_before_insert)
        event.listen(cls, "before_update", mptt_before_update)
        event.listen(cls, "before_delete", mptt_before_delete)

    # Minimal schema
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def parent_id(cls):
        return Column("parent_id", Integer, ForeignKey(f"{cls.__tablename__}.id"))

    @declared_attr
    def parent(cls):
        return relationship(cls, backref=backref("children", cascade="all,delete"))

    @declared_attr
    def left(cls):
        return Column("lft", Integer)

    @declared_attr
    def right(cls):
        return Column("rgt", Integer)

    @declared_attr
    def level(cls):
        return Column("level", Integer)

    @declared_attr
    def tree_id(cls):
        return Column("tree_id", Integer)
