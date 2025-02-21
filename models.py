from datetime import datetime
from db.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Owners(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)


class Pets(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    breed = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("owners.id"))
