# diffs/compare_diffs.py

from sqlalchemy import Column, Integer, String, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import configure_mappers
from sqlalchemy_mptt.events import mptt_before_insert, mptt_before_update, mptt_before_delete

# Import BaseNestedSets classes from each diff
from diff1 import BaseNestedSets as Base1
from diff2 import BaseNestedSets as Base2
from diff3 import BaseNestedSets as Base3
from diff4 import BaseNestedSets as Base4

Base = declarative_base()

# Define real mapped subclasses to trigger SQLAlchemy mapper hooks
class Sub1(Base1, Base):
    __tablename__ = 'sub1'
    id = Column(Integer, primary_key=True)

class Sub2(Base2, Base):
    __tablename__ = 'sub2'
    id = Column(Integer, primary_key=True)

class Sub3(Base3, Base):
    __tablename__ = 'sub3'
    id = Column(Integer, primary_key=True)

class Sub4(Base4, Base):
    __tablename__ = 'sub4'
    id = Column(Integer, primary_key=True)

# Force mapper configuration to trigger any SQLAlchemy lifecycle events
configure_mappers()

def check(cls, label):
    print(f"\nChecking {label}...")
    for event_type, handler in [
        ("before_insert", mptt_before_insert),
        ("before_update", mptt_before_update),
        ("before_delete", mptt_before_delete)
    ]:
        attached = event.contains(cls, event_type, handler)
        print(f"  {event_type:<15}: {'registered' if attached else 'NOT registered'}")

# Run the checks
check(Sub1, "Diff 1")
check(Sub2, "Diff 2")
check(Sub3, "Diff 3")
check(Sub4, "Diff 4")
