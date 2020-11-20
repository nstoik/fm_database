# -*- coding: utf-8 -*-
"""Message model for farm monitor."""
from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, PickleType, String
from sqlalchemy.sql import func

from ..database import Model, SurrogatePK


class Message(Model, SurrogatePK):
    """A message sent between devices."""

    __tablename__ = 'message'

    source = Column(String(20))
    destination = Column(String(20))
    classification = Column(String(20))

    created_at = Column(DateTime, default=func.now())
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)

    payload = Column(PickleType, default=None)

    def __init__(self, source, destination, classification):
        """Create an instance."""
        self.source = source
        self.destination = destination
        self.classification = classification
        return

    def set_datetime(self, valid_from=False, valid_to=False):
        """Set the valid_from and valid_to dates. Input must be a timedelta object."""

        if not valid_to:
            valid_to = timedelta(days=1)

        if not valid_from:
            valid_from = timedelta(seconds=0)

        self.valid_from = datetime.now() + valid_from
        self.valid_to = datetime.now() + valid_to

        return
