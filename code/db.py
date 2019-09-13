from sqlalchemy import (
    Column, Integer, String, DateTime, Float,
    Boolean, PrimaryKeyConstraint, Index,
)
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def make_time_column():
    return Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Hero(db.Model):
    __tablename__ = 'heroes'
    __table_args__ = (
        PrimaryKeyConstraint('email', 'lang', name='hero_key'),
        Index('hero_email_key', 'email'),
        Index('hero_nick_key', 'nick'),
        Index('hero_lang_key', 'lang'),
    )

    email = Column(String, nullable=False)
    nick = Column(String, nullable=False)
    lang = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    contest_consent = Column(Boolean, nullable=False)
    marketing_consent = Column(Boolean, nullable=False)
    time = make_time_column()

    def __init__(self, email, nick, lang, score=0, contest_consent=True, marketing_consent=False):
        self.email = email
        self.nick = nick
        self.lang = lang
        self.score = score
        self.contest_consent = contest_consent
        self.marketing_consent = marketing_consent


class ScoreLog(db.Model):
    __tablename__ = 'score_logs'
    __table_args__ = (
        Index('score_logs_email_key', 'email'),
        Index('score_logs_lang_key', 'lang'),
    )

    pk = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    lang = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    execution_time = Column(Float, nullable=False)
    fail = Column(Boolean, nullable=False)
    time = make_time_column()

    def __init__(self, email, lang, fail, execution_time, score):
        self.email = email
        self.lang = lang
        self.score = score
        self.fail = fail
        self.execution_time = execution_time
