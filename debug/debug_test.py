from sqlalchemy import Column, Integer, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from after.mixins_after import BaseNestedSets
from sqlalchemy_mptt.events import mptt_before_insert

Base = declarative_base()

class DebugTree(Base, BaseNestedSets):
    __tablename__ = "debug_tree"
    id = Column(Integer, primary_key=True)

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

print("Registered before_insert:", event.contains(DebugTree, "before_insert", mptt_before_insert))

node = DebugTree(id=1)
session.add(node)
session.commit()

print("Node created. MPTT fields:")
print("left:", node.left)
print("right:", node.right)
print("level:", node.level)
print("tree_id:", node.tree_id)
