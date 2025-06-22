from sqlalchemy import Column, event, ForeignKey, Index, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.mapper import Mapper

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
        if hasattr(cls, '__mapper__'):
            cls.__mapper__.batch = False

@event.listens_for(Mapper, "mapper_configured")
def auto_register_mptt(mapper, cls):
    if issubclass(cls, BaseNestedSets) and cls is not BaseNestedSets:
        if not event.contains(cls, "before_insert", mptt_before_insert):
            cls.register_tree()

@classmethod
def register_tree(cls):
    event.listen(cls, "before_insert", mptt_before_insert)
    event.listen(cls, "before_update", mptt_before_update)
    event.listen(cls, "before_delete", mptt_before_delete)

BaseNestedSets.register_tree = register_tree

# Schema attributes (same as before)
for name, col in {
    "id": Column(Integer, primary_key=True),
    "parent_id": Column("parent_id", Integer),
    "left": Column("lft", Integer),
    "right": Column("rgt", Integer),
    "level": Column("level", Integer),
    "tree_id": Column("tree_id", Integer),
}.items():
    setattr(BaseNestedSets, name, declared_attr(lambda cls, col=col: col))

setattr(BaseNestedSets, "parent", declared_attr(
    lambda cls: relationship(cls, backref=backref("children", cascade="all,delete"))
))
