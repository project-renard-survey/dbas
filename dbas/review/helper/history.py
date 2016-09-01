"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import dbas.user_management as _user_manager
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, LastReviewerDelete, ReviewOptimization, LastReviewerOptimization, \
    User, ReputationHistory, ReputationReason
from dbas.lib import sql_timestamp_pretty_print, get_public_nickname_based_on_settings
from dbas.review.helper.reputation import get_reputation_of, reputation_borders, reputation_icons
from sqlalchemy import and_


def get_complete_review_history(mainpage, nickname, translator):
    """

    :param nickname:
    :return:
    """
    ret_dict = dict()
    ret_dict['has_access'] = __has_access_to_history(nickname)

    deletes_list = __get_executed_reviews_of(mainpage, ReviewDelete, LastReviewerDelete, translator.get_lang())
    optimizations_list = __get_executed_reviews_of(mainpage, ReviewOptimization, LastReviewerOptimization, translator.get_lang())

    past_decision = [{
        'title': 'Delete Queue',
        'icon': reputation_icons['deletes'],
        'queue': 'deletes',
        'content': deletes_list,
    }, {
        'title': 'Optimization Queue',
        'queue': reputation_icons['optimizations'],
        'icon': 'fa fa-flag',
        'content': optimizations_list
    }]
    ret_dict['past_decision'] = past_decision

    return ret_dict


def get_reputation_history_of(nickname, translator):
    """

    :param nickname:
    :param translator:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return dict()

    ret_dict = dict()
    count, all_rights = get_reputation_of(nickname)
    ret_dict['count'] = count
    ret_dict['all_rights'] = all_rights

    db_reputation = DBDiscussionSession.query(ReputationHistory) \
        .filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .order_by(ReputationHistory.uid.asc())\
        .all()

    rep_list = list()
    for rep in db_reputation:
        date = sql_timestamp_pretty_print(rep.timestamp, translator.get_lang(), humanize=False)
        points_data = '<span class="success-description points">+' if rep.reputations.points > 0 else '<span class="error-description points">'
        points_data += str(rep.reputations.points) + '</span'
        points = rep.reputations.points
        action = translator.get(rep.reputations.reason)
        rep_list.append({'date': date, 'points_data': points_data, 'action': action, 'points': points})

    ret_dict['history'] = rep_list

    return ret_dict


def __get_executed_reviews_of(mainpage, table_type, last_review_type, lang):
    """
    Returns array with all relevant information about the last reviews of the given table.

    :param mainpage: Mainpage of D-BAS
    :param table_type: Type of the review table
    :param last_review_type: Type of the last reviewer of the table
    :param lang: current ui_locales
    :return: Array with all decision per table
    """
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == True).order_by(table_type.uid.desc()).all()

    for review in db_reviews:
        # getting all pro and contra votes for this review
        pro_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay == True)).all()
        con_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay == False)).all()
        # getting the users which have voted
        pro_list = list()
        con_list = list()
        for pro in pro_votes:
            pro_list.append(__get_user_dict_for_review(pro.reviewer_uid, mainpage))
        for con in con_votes:
            con_list.append(__get_user_dict_for_review(con.reviewer_uid, mainpage))

        # and build up some dict
        entry = dict()
        entry['entry_id'] = review.uid
        entry['pro'] = pro_list
        entry['con'] = con_list
        entry['timestamp'] = sql_timestamp_pretty_print(review.timestamp, lang)
        entry['votes_pro'] = pro_list
        entry['votes_con'] = con_list
        some_list.append(entry)

    return some_list


def __get_user_dict_for_review(user_id, mainpage):
    """
    Fetches some data of the given user.

    :param mainpage: Mainpage of D-BAS
    :return: dcit with gravatar, uerpage and nickname
    """
    db_user = DBDiscussionSession.query(User).filter_by(uid=user_id).first()
    image_url = _user_manager.get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': get_public_nickname_based_on_settings(db_user),
        'userpage_url': mainpage + '/user/' + get_public_nickname_based_on_settings(db_user)
    }


def __has_access_to_history(nickname):
    """

    :param nickname:
    :return:
    """
    reputation_count, is_user_author = get_reputation_of(nickname)
    return is_user_author or reputation_count > reputation_borders['history']