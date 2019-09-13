from logging import getLogger
from datetime import datetime
from usernames import random_name

from const import TOP_HIDE_SCORES, MAX_SCORES_ON_MAIN_PAGE
from db import db, Hero, ScoreLog

logger = getLogger('app')


def get_heroes(without_limit=False, hide_scores=True):
    query = (
        Hero.query
        .order_by(Hero.score, Hero.time)
    )

    if not without_limit:
        query = query.limit(MAX_SCORES_ON_MAIN_PAGE)
        count_empty_heroes = (MAX_SCORES_ON_MAIN_PAGE - query.count())
    else:
        count_empty_heroes = 0

    scores = list(query.all())
    if hide_scores:
        for hero in scores[0:TOP_HIDE_SCORES]:
            hero.score = '???'

    empty_heroes = [Hero('-', '-', '-')] * count_empty_heroes
    return scores + empty_heroes


def submit_score(email, lang, code, contest_consent, marketing_consent, execution_time=0.0):
    hero = Hero.query.filter_by(email=email).first()
    new_score = len(code)
    if hero is None:
        old_score = '-'
        nick = random_name()
        hero = Hero(email, nick, lang, new_score, contest_consent, marketing_consent)
    else:
        old_score = hero.score
        if old_score < new_score:
            logger.warning(
                'Worse Record[%r, %s] in %0.2f seconds, from %s to %s',
                email, lang, execution_time, old_score, new_score,
            )
            return
        hero.score = new_score
        hero.lang = lang
        hero.contest_consent = contest_consent
        hero.marketing_consent = marketing_consent

    logger.info(
        'New Record[%r, %s] in %0.2f seconds, from %s to %s',
        email, lang, execution_time, old_score, new_score,
    )

    db.session.add(hero)
    db.session.commit()


def add_score_log(email, lang, code, fail=False, execution_time=0.0):
    log = ScoreLog(
        email=email,
        lang=lang,
        score=len(code),
        fail=fail,
        execution_time=execution_time,
    )

    db.session.add(log)
    db.session.commit()


def get_score_logs(page=1, limit=60):
    pre_page = page - 1

    count = ScoreLog.query.count()
    query = (
        ScoreLog.query
        .order_by(ScoreLog.pk.desc())
        .offset(pre_page * limit)
        .limit(limit) 
    )

    return list(query.all()), count


def get_username_by_email(email):
    hero = Hero.query.filter_by(email=email).first()
    if hero is None:
        return 'not here yet'
    else:
        return hero.nick
