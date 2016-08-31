"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from sqlalchemy import and_

from dbas.helper.relation import RelationHelper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, VoteArgument
from dbas.logger import logger


def get_attack_for_argument(argument_uid, lang, restriction_on_attacks=None, restriction_on_arg_uids=[], last_attack=None, history=None):
    """
    Selects an attack out of the web of reasons.

    :param argument_uid: Argument.uid
    :param lang: ui_locales
    :param restriction_on_attacks: String
    :param restriction_on_arg_uids: Argument.uid
    :param last_attack: String
    :param history: History
    :return: Argument.uid, String, Boolean if no new attacks are found
    """
    # getting undermines or undercuts or rebuts
    logger('RecommenderSystem', 'get_attack_for_argument', 'main ' + str(argument_uid) + ' (reststriction: ' +
           str(restriction_on_attacks) + ', ' + str(restriction_on_arg_uids) + ')')

    redirected_from_jump = False
    if history:
        history = history.split('-')
        redirected_from_jump = 'jump' in history[-2 if len(history) > 1 else -1]
    # TODO COMMA16 Special Case (forbid: undercuts of undercuts)
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
    is_current_arg_undercut = db_argument.argument_uid is not None
    tmp = restriction_on_attacks if restriction_on_attacks else ''
    restriction_on_attacks = [tmp, 'undercut' if is_current_arg_undercut and not redirected_from_jump else '']
    logger('RecommenderSystem', 'get_attack_for_argument', 'restriction  1: ' + restriction_on_attacks[0] +
           ', restriction  2: ' + restriction_on_attacks[1])

    attacks_array, key, no_new_attacks = __get_attack_for_argument(argument_uid, lang, restriction_on_attacks,
                                                                   restriction_on_arg_uids, last_attack, history)
    if not attacks_array or len(attacks_array) == 0:
        if no_new_attacks:
            return 0, 'end_attack'
        else:
            return 0, 'end'
    else:
        attack_no = random.randrange(0, len(attacks_array))  # Todo fix random
        attack_uid = attacks_array[attack_no]['id']

        logger('RecommenderSystem', 'get_attack_for_argument', 'main return ' + key + ' by ' + str(attack_uid))

        return attack_uid, key


def get_argument_by_conclusion(statement_uid, is_supportive):
    """
    Returns a random argument by its conclusion

    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :return: Argument
    """
    logger('RecommenderSystem', 'get_argument_by_conclusion', 'statement: ' + str(statement_uid) + ', supportive: ' + str(is_supportive))
    db_arguments = get_arguments_by_conclusion(statement_uid, is_supportive)
    DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive, Argument.conclusion_uid == statement_uid)).all()

    if not db_arguments:
        return 0
    rnd = random.randint(0, len(db_arguments) - 1)  # TODO fix random
    return db_arguments[0 if len(db_arguments) == 1 else rnd].uid


def get_arguments_by_conclusion(statement_uid, is_supportive):
    """
    Returns all arguments by their conclusion

    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :return: [Argument]
    """
    logger('RecommenderSystem', 'get_argument_by_conclusion', 'statement: ' + str(statement_uid) + ', supportive: ' + str(is_supportive))
    db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
                                                                   Argument.conclusion_uid == statement_uid)).all()

    if not db_arguments:
        return None

    logger('RecommenderSystem', 'get_argument_by_conclusion', 'found ' + str(len(db_arguments)) + ' arguments')
    # TODO sort arguments and return a subset

    return db_arguments


def __get_attack_for_argument(argument_uid, lang, restriction_on_attacks, restriction_on_argument_uids,
                              last_attack, history):
    """
    Returns a dictionary with attacks. The attack itself is random out of the set of attacks, which were not done yet.
    Additionally returns id's of premises groups with [key + str(index) + 'id']

    :param argument_uid: Argument.uid
    :param lang: ui_locales
    :param restriction_on_attacks: String
    :param restriction_on_argument_uids: Argument.uid
    :param last_attack: String
    :param history: History
    :return: [Argument.uid], String, Boolean if no new attacks are found
    """

    # 1 = undermine, 2 = support, 3 = undercut, 4 = overbid, 5 = rebut, all possible attacks

    complete_list_of_attacks = [1, 3, 5]
    attacks = [1, 3, 5]

    logger('RecommenderSystem', '__get_attack_for_argument', 'attack_list : ' + str(attacks))
    attack_list = complete_list_of_attacks if len(attacks) == 0 else attacks
    return_array, key, no_new_attacks = __get_attack_for_argument_by_random_in_range(argument_uid, attack_list,
                                                                                     complete_list_of_attacks,
                                                                                     lang, restriction_on_attacks,
                                                                                     restriction_on_argument_uids,
                                                                                     last_attack, history)

    # sanity check if we could not found an attack for a left attack in out set
    if not return_array and len(attacks) > 0:
        return_array, key, no_new_attacks = __get_attack_for_argument_by_random_in_range(argument_uid, [],
                                                                                         complete_list_of_attacks,
                                                                                         lang, restriction_on_attacks,
                                                                                         restriction_on_argument_uids,
                                                                                         last_attack,
                                                                                         history)

    return return_array, key, no_new_attacks


def __get_attack_for_argument_by_random_in_range(argument_uid, attack_list, list_of_all_attacks, lang,
                                                 restriction_on_attacks, restriction_on_argument_uids, last_attack,
                                                 history):
    """

    :param argument_uid: Argument.uid
    :param attack_list:
    :param list_of_all_attacks:
    :param lang: ui_locales
    :param restriction_on_attacks: String
    :param restriction_on_argument_uids: Argument.uid
    :param last_attack: String
    :param history: History
    :return: [Argument.uid], String, Boolean if no new attacks are found
    """
    return_array    = None
    key             = ''
    left_attacks    = list(set(list_of_all_attacks) - set(attack_list))
    attack_found    = False
    is_supportive   = False
    is_attack_in_history  = False
    _rh = RelationHelper(argument_uid, lang)

    logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'argument_uid: Argument.uid ' + str(argument_uid) +
           ', attack_list : ' + str(attack_list) +
           ', complete_list_of_attacks : ' + str(list_of_all_attacks) +
           ', left_attacks : ' + str(left_attacks))

    # randomize at least 1, maximal 3 times for getting an attack or
    # if the attack type and the only attacking argument are the same as the restriction
    while len(attack_list) > 0:
        attack = random.choice(attack_list)
        attack_list.remove(attack)

        if attack == 1:
            key = 'undermine'
            return_array = _rh.get_undermines_for_argument_uid(is_supportive)
            # special case when undermining an undermine
            is_supportive = last_attack == 'undermine'

        elif attack == 5:
            key = 'rebut'
            return_array = _rh.get_rebuts_for_argument_uid()

        else:
            key = 'undercut'
            return_array = _rh.get_undercuts_for_argument_uid()

        if return_array and len(return_array) != 0:
            # check if the step is already in history
            new_attack_step = str(argument_uid) + '/' + str(key) + '/' + str(return_array[0]['id'])
            is_attack_in_history = new_attack_step in str(history)

            if str(key) not in restriction_on_attacks \
                    and return_array[0]['id'] not in restriction_on_argument_uids \
                    and not is_attack_in_history:  # no duplicated attacks
                logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'attack found for key: ' + key)
                attack_found = True
                break
            else:
                logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'attack \'' + key + '\' is restricted')
                key = ''
                return_array = []
        else:
            logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'no attack found for key: ' + key)

    if len(left_attacks) > 0 and not attack_found:
        logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'redo algo with left attacks ' + str(left_attacks))
        return_array, key, is_attack_in_history = __get_attack_for_argument_by_random_in_range(argument_uid, left_attacks,
                                                                                               left_attacks, lang,
                                                                                               restriction_on_attacks,
                                                                                               restriction_on_argument_uids,
                                                                                               last_attack, history)
    else:
        if len(left_attacks) == 0:
            logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'no attacks left for redoing')
        if attack_found:
            logger('RecommenderSystem', '__get_attack_for_argument_by_random_in_range', 'attack found')

    return return_array, key, is_attack_in_history


def __get_best_argument(argument_list):
    """

    :param argument_list: Argument[]
    :return: Argument
    """
    logger('RecommenderSystem', '__get_best_argument', 'main')
    evaluations = []
    for argument in argument_list:
        evaluations.append(__evaluate_argument(argument.uid))

    best = max(evaluations)
    index = [i for i, j in enumerate(evaluations) if j == best]
    return index[0]


def __evaluate_argument(argument_uid):
    """

    :param argument_uid: Argument.uid Argument.uid
    :return:
    """
    logger('RecommenderSystem', '__evaluate_argument', 'argument ' + str(argument_uid))

    db_votes = DBDiscussionSession.query(VoteArgument).filter_by(argument_uid=argument_uid).all()
    db_valid_votes   = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
                                                                           VoteArgument.is_valid == True)).all()
    db_valid_upvotes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
                                                                           VoteArgument.is_valid == True,
                                                                           VoteArgument.is_up_vote == True)).all()
    votes = len(db_votes)
    valid_votes = len(db_valid_votes)
    valid_upvotes = len(db_valid_upvotes)
    all_users = len(DBDiscussionSession.query(User).all())

    index_up_vs_down = valid_upvotes / (1 if valid_votes == 0 else valid_votes)
    index_participation = votes / (1 if all_users == 0 else all_users)

    return index_participation, index_up_vs_down
