# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 14:28:00
# Database: sqlite:////tmp/tmp.tEbuKDkipq-01JGBZCPHQVDTZCXAA43CGDWVS/EurovisionDatabase/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Country(Base):  # type: ignore
    """
    description: Stores details about countries participating in the Eurovision contest.
    """
    __tablename__ = 'country'
    _s_collection_name = 'Country'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    flag_image = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ContestantList : Mapped[List["Contestant"]] = relationship(back_populates="country")
    HostList : Mapped[List["Host"]] = relationship(back_populates="country")
    JudgeList : Mapped[List["Judge"]] = relationship(back_populates="country")



class Event(Base):  # type: ignore
    """
    description: Records details of Eurovision events held annually.
    """
    __tablename__ = 'event'
    _s_collection_name = 'Event'  # type: ignore

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    EventParticipationList : Mapped[List["EventParticipation"]] = relationship(back_populates="event")
    JuryList : Mapped[List["Jury"]] = relationship(back_populates="event")
    AudienceVoteList : Mapped[List["AudienceVote"]] = relationship(back_populates="event")
    PerformanceList : Mapped[List["Performance"]] = relationship(back_populates="event")



class Contestant(Base):  # type: ignore
    """
    description: Stores details of contestants participating in the Eurovision contest.
    """
    __tablename__ = 'contestant'
    _s_collection_name = 'Contestant'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(ForeignKey('country.id'))
    bio = Column(String)

    # parent relationships (access parent)
    country : Mapped["Country"] = relationship(back_populates=("ContestantList"))

    # child relationships (access children)
    EventParticipationList : Mapped[List["EventParticipation"]] = relationship(back_populates="contestant")
    SongList : Mapped[List["Song"]] = relationship(back_populates="contestant")



class Host(Base):  # type: ignore
    """
    description: Stores information about the hosts of the Eurovision contest.
    """
    __tablename__ = 'host'
    _s_collection_name = 'Host'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(ForeignKey('country.id'))
    years_hosted = Column(Integer)

    # parent relationships (access parent)
    country : Mapped["Country"] = relationship(back_populates=("HostList"))

    # child relationships (access children)



class Judge(Base):  # type: ignore
    """
    description: Stores details about judges in the Eurovision contest.
    """
    __tablename__ = 'judge'
    _s_collection_name = 'Judge'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(ForeignKey('country.id'))
    experience_years = Column(Integer)

    # parent relationships (access parent)
    country : Mapped["Country"] = relationship(back_populates=("JudgeList"))

    # child relationships (access children)
    JuryList : Mapped[List["Jury"]] = relationship(back_populates="judge")
    VoteList : Mapped[List["Vote"]] = relationship(back_populates="judge")



class EventParticipation(Base):  # type: ignore
    """
    description: Links contestants to the events they participate in.
    """
    __tablename__ = 'event_participation'
    _s_collection_name = 'EventParticipation'  # type: ignore

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('event.id'))
    contestant_id = Column(ForeignKey('contestant.id'))

    # parent relationships (access parent)
    contestant : Mapped["Contestant"] = relationship(back_populates=("EventParticipationList"))
    event : Mapped["Event"] = relationship(back_populates=("EventParticipationList"))

    # child relationships (access children)



class Jury(Base):  # type: ignore
    """
    description: Associates judges with the events they are judging.
    """
    __tablename__ = 'jury'
    _s_collection_name = 'Jury'  # type: ignore

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('event.id'))
    judge_id = Column(ForeignKey('judge.id'))

    # parent relationships (access parent)
    event : Mapped["Event"] = relationship(back_populates=("JuryList"))
    judge : Mapped["Judge"] = relationship(back_populates=("JuryList"))

    # child relationships (access children)



class Song(Base):  # type: ignore
    """
    description: Stores information about songs that contestants perform.
    """
    __tablename__ = 'song'
    _s_collection_name = 'Song'  # type: ignore

    id = Column(Integer, primary_key=True)
    title = Column(String)
    duration = Column(Integer)
    contestant_id = Column(ForeignKey('contestant.id'))
    language = Column(String)

    # parent relationships (access parent)
    contestant : Mapped["Contestant"] = relationship(back_populates=("SongList"))

    # child relationships (access children)
    AudienceVoteList : Mapped[List["AudienceVote"]] = relationship(back_populates="song")
    PerformanceList : Mapped[List["Performance"]] = relationship(back_populates="song")
    VoteList : Mapped[List["Vote"]] = relationship(back_populates="song")
    VoteSummaryList : Mapped[List["VoteSummary"]] = relationship(back_populates="song")



class AudienceVote(Base):  # type: ignore
    """
    description: Records audience votes for songs performed in events.
    """
    __tablename__ = 'audience_vote'
    _s_collection_name = 'AudienceVote'  # type: ignore

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('event.id'))
    song_id = Column(ForeignKey('song.id'))
    points = Column(Integer)

    # parent relationships (access parent)
    event : Mapped["Event"] = relationship(back_populates=("AudienceVoteList"))
    song : Mapped["Song"] = relationship(back_populates=("AudienceVoteList"))

    # child relationships (access children)



class Performance(Base):  # type: ignore
    """
    description: Stores details about performances in the Eurovision events.
    """
    __tablename__ = 'performance'
    _s_collection_name = 'Performance'  # type: ignore

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('event.id'))
    song_id = Column(ForeignKey('song.id'))
    performance_time = Column(DateTime)

    # parent relationships (access parent)
    event : Mapped["Event"] = relationship(back_populates=("PerformanceList"))
    song : Mapped["Song"] = relationship(back_populates=("PerformanceList"))

    # child relationships (access children)



class Vote(Base):  # type: ignore
    """
    description: Records votes given by judges to songs performed by contestants.
    """
    __tablename__ = 'vote'
    _s_collection_name = 'Vote'  # type: ignore

    id = Column(Integer, primary_key=True)
    judge_id = Column(ForeignKey('judge.id'))
    song_id = Column(ForeignKey('song.id'))
    points = Column(Integer)
    vote_time = Column(DateTime)

    # parent relationships (access parent)
    judge : Mapped["Judge"] = relationship(back_populates=("VoteList"))
    song : Mapped["Song"] = relationship(back_populates=("VoteList"))

    # child relationships (access children)



class VoteSummary(Base):  # type: ignore
    """
    description: Stores the total points received by each song, calculated manually.
    """
    __tablename__ = 'vote_summary'
    _s_collection_name = 'VoteSummary'  # type: ignore

    id = Column(Integer, primary_key=True)
    song_id = Column(ForeignKey('song.id'))
    total_points = Column(Integer)

    # parent relationships (access parent)
    song : Mapped["Song"] = relationship(back_populates=("VoteSummaryList"))

    # child relationships (access children)
