import unittest
from sqlalchemy import Column, Integer, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from after.mixins_after import BaseNestedSets
from sqlalchemy_mptt.events import mptt_before_insert

Base = declarative_base()

class TestTree(Base, BaseNestedSets):
    __tablename__ = "test_tree"
    id = Column(Integer, primary_key=True)

class AutoRegistrationTest(unittest.TestCase):
    def test_event_registration(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        self.assertTrue(
            event.contains(TestTree, "before_insert", mptt_before_insert),
            "Auto-registration failed: before_insert not registered"
        )

if __name__ == "__main__":
    unittest.main()
