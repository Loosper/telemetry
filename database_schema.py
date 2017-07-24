#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint,\
    create_engine

Base = declarative_base()


# TODO: relationships
class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, unique=True)
    # date type if db supports it
    delivery_date = Column(String(25), nullable=False)
    provider = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    model = Column(String(20), nullable=False)
    serial = Column(Integer, nullable=False)

    def serialise(self):
        return {
            'id': self.id,
            'delivery_date': self.delivery_date,
            'provider': self.provider,
            'type': self.type,
            'model': self.model,
            'serial': self.serial
        }


class Sim(Base):
    __tablename__ = 'sims'

    id = Column(Integer, primary_key=True, unique=True)
    # date type if db supports it
    delivery_date = Column(String(25), nullable=False)
    carrier = Column(String(20), nullable=False)
    number = Column(String(15), nullable=False)

    def serialise(self):
        return {
            'id': self.id,
            'delivery_date': self.delivery_date,
            'carrier': self.carrier,
            'number': self.number
        }


# sim and device should be a reference to a row
class Couple(Base):
    __tablename__ = 'couples'
    __table_args__ = (UniqueConstraint('device_id', 'sim_id'),)

    # auto increment this
    id = Column(Integer, primary_key=True, unique=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    sim_id = Column(Integer, ForeignKey('sims.id'))
    # date type if db supports it
    couple_date = Column(String(25), nullable=False)
    assigned_to = Column(String(25), nullable=False)
    # add relationships

    # one to one relationship, does it need a backref?
    sim = relationship('Sim', uselist=False)
    device = relationship('Device', uselist=False)

    def serialise(self):
        return {
            'id': self.id,
            'couple_date': self.couple_date,
            'assigned_to': self.assigned_to,
            'device_id': self.device_id,
        }


engine = create_engine('sqlite:///database.sql', echo=False)
Session = sessionmaker(bind=engine)

# launching this by itself probably means to remake the database
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
