import random

import transaction
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Argument, Premise, MarkedArgument, ClickedArgument, \
    sql_timestamp_pretty_print, ClickedStatement, Statement
from dbas.handler import user, notification as NotificationHelper
from dbas.handler.statements import insert_new_premises_for_argument
from dbas.helper.query import statement_min_length
from dbas.input_validator import get_relation_between_arguments
from dbas.input_validator import is_integer
from dbas.lib import get_slug_by_statement_uid, get_all_arguments_with_text_and_url_by_statement_id, \
    get_profile_picture, get_text_for_argument_uid
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_new_statement, rep_reason_first_new_argument
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager, get_url_for_new_argument


def set_arguments_premises(for_api, data) -> dict:
    """
    Set new premise for a given conclusion and returns dictionary with url for the next step of the discussion

    :param for_api: boolean if requests came via the API
    :param data: dict if requests came via the API
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    try:
        nickname = data['nickname']
        premisegroups = data['statement']
        issue_id = data['issue_id']
        arg_uid = data['arg_uid']
        attack_type = data['attack_type']
        history = data['history'] if '_HISTORY_' in data else None
        mailer = data['mailer'] if 'mailer' in data else None
        port = data['port'] if 'port' in data else None
        discussion_lang = data['discussion_lang'] if 'discussion_lang' in data else DBDiscussionSession.query(Issue).get(issue_id).lang
        default_locale_name = data['default_locale_name'] if 'default_locale_name' in data else discussion_lang
        application_url = data['application_url']
    except KeyError as e:
        logger('ArgumentsHelper', 'arguments_premises', repr(e), error=True)
        _tn = Translator('en')
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    # escaping will be done in QueryHelper().set_statement(...)
    url, statement_uids, error = __process_input_of_premises_for_arguments_and_receive_url(default_locale_name, arg_uid,
                                                                                           attack_type, premisegroups,
                                                                                           issue_id, nickname, for_api,
                                                                                           application_url,
                                                                                           discussion_lang, history,
                                                                                           port, mailer)
    user.update_last_action(nickname)

    prepared_dict = dict()
    prepared_dict['error'] = error
    prepared_dict['statement_uids'] = statement_uids

    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_new_argument)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        url += '#access-review'
        prepared_dict['url'] = url

    if url == -1:
        return prepared_dict

    prepared_dict['url'] = url

    logger('ArgumentsHelper', 'set_new_premises_for_argument', 'returning {}'.format(prepared_dict))
    return prepared_dict


def get_all_infos_about_argument(uid, application_url, nickname, ui_locales) -> dict:
    """
    Returns bunch of information about the given argument

    :param uid: ID of the argument
    :param application_url: url of the application
    :param nickname: current users nickname
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: dictionary with many information or an error
    """

    _t = Translator(ui_locales)

    if not is_integer(uid):
        prepared_dict = {'error': _t.get(_.internalError)}
    else:
        prepared_dict = __get_infos_about_argument(uid, application_url, nickname, _t)
        prepared_dict['error'] = ''

    return prepared_dict


def __get_infos_about_argument(uid, main_page, nickname, _t):
    """
    Returns several infos about the argument.

    :param uid: Argument.uid
    :param main_page: url
    :param nickname: current nickname
    :param _t: Translator
    :return: dict()
    """
    return_dict = dict()
    db_votes = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == uid,
                                                                      ClickedArgument.is_valid == True,
                                                                      ClickedStatement.is_up_vote == True)).all()
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return return_dict

    db_author = DBDiscussionSession.query(User).get(db_argument.author_uid)
    return_dict['vote_count'] = str(len(db_votes))
    return_dict['author'] = db_author.get_global_nickname()
    return_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    return_dict['gravatar'] = get_profile_picture(db_author)
    return_dict['timestamp'] = sql_timestamp_pretty_print(db_argument.timestamp, db_argument.lang)
    text = get_text_for_argument_uid(uid)
    return_dict['text'] = text[0:1].upper() + text[1:] + '.'

    supporters = []
    gravatars = dict()
    public_page = dict()
    for vote in db_votes:
        db_user = DBDiscussionSession.query(User).get(vote.author_uid)
        name = db_user.get_global_nickname()
        if db_user.nickname == nickname:
            name += ' (' + _t.get(_.itsYou) + ')'
        supporters.append(name)
        gravatars[name] = get_profile_picture(db_user)
        public_page[name] = main_page + '/user/' + str(db_user.uid)

    return_dict['supporter'] = supporters
    return_dict['gravatars'] = gravatars
    return_dict['public_page'] = public_page

    return return_dict


def get_arguments_by_statement_uid(uid, application_url, ui_locales) -> dict:
    """
    Collects every argument which uses the given statement

    :param uid: ID of statement to request all arguments
    :param application_url: url of the application
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: prepared collection with several arguments
    """
    if not is_integer(uid):
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError)}

    slug = get_slug_by_statement_uid(uid)
    _um = UrlManager(application_url, slug)
    prepared_dict = dict()
    prepared_dict['arguments'] = get_all_arguments_with_text_and_url_by_statement_id(uid, _um, True, is_jump=True)
    prepared_dict['error'] = ''

    return prepared_dict


def __process_input_of_premises_for_arguments_and_receive_url(default_locale_name, arg_id, attack_type, premisegroups,
                                                              issue, user, for_api, application_url, discussion_lang,
                                                              history, port, mailer):
    """
    Inserts the given text in premisegroups as new arguments in dependence of the input parameters and returns a URL for forwarding.

    .. note::

        Optimize the "for_api" part

    :param default_locale_name: Default lang of the app
    :param arg_id: Argument.uid
    :param attack_type: String
    :param premisegroups: [Strings]
    :param issue: Issue.uid
    :param user: User.nickname
    :param for_api: Boolean
    :param application_url: URL
    :param discussion_lang: ui_locales
    :param history: History of the user
    :param port: Port of notification server
    :param mailer: Instance of pyramid mailer
    :return: URL, [Statement.uids], String
    """
    logger('ArgumentsHelper', 'process_input_of_premises_for_arguments_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    _tn = Translator(discussion_lang)
    if not db_user:
        return '', '', _tn.get(_.userNotFound)

    slug = DBDiscussionSession.query(Issue).get(issue).slug
    error = ''
    supportive = attack_type == 'support' or attack_type == 'overbid'

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    for group in premisegroups:  # premise groups is a list of lists
        new_argument = insert_new_premises_for_argument(application_url, default_locale_name, group, attack_type,
                                                        arg_id, issue, user, discussion_lang)
        if not isinstance(new_argument, Argument):  # break on error
            a = _tn.get(_.notInsertedErrorBecauseEmpty)
            b = _tn.get(_.minLength)
            c = str(statement_min_length)
            d = _tn.get(_.eachStatement)
            error = '{} ({}: {} {})'.format(a, b, c, d)
            return -1, None, error

        new_argument_uids.append(new_argument.uid)

    statement_uids = []
    if for_api:
        # @OPTIMIZE
        # Query all recently stored premises (internally: statements) and collect their ids
        # This is a bad workaround, let's just think about it in future.
        for uid in new_argument_uids:
            current_pgroup = DBDiscussionSession.query(Argument).get(uid).premisesgroup_uid
            current_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_pgroup).all()
            for premise in current_premises:
                statement_uids.append(premise.statement_uid)

    # #arguments=0: empty input
    # #arguments=1: deliver new url
    # #arguments>1: deliver url where the user has to choose between her inputs
    _um = url = UrlManager(application_url, slug, for_api, history)
    if len(new_argument_uids) == 0:
        error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength), statement_min_length)

    elif len(new_argument_uids) == 1:
        url = get_url_for_new_argument(new_argument_uids, history, discussion_lang, _um)

    else:
        url = __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type,
                                                                                    arg_id, _um, supportive)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        # add marked arguments
        DBDiscussionSession.add_all([MarkedArgument(argument=uid, user=db_user.uid) for uid in new_argument_uids])
        DBDiscussionSession.flush()
        transaction.commit()

        new_uid = random.choice(new_argument_uids)   # TODO eliminate random
        attack = get_relation_between_arguments(arg_id, new_uid)

        tmp_url = _um.get_url_for_reaction_on_argument(False, arg_id, attack, new_uid)

        NotificationHelper.send_add_argument_notification(tmp_url, arg_id, user, port, mailer)

    return url, statement_uids, error


def __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type, arg_id, _um, supportive):
    """
    Return the 'choose' url, when the user entered more than one premise for an argument

    :param new_argument_uids: [Argument.uid]
    :param attack_type: String
    :param arg_id: Argument.uid
    :param _um: UrlManager
    :param supportive: Boolean
    :return: String
    """
    pgroups = []
    url = ''
    for uid in new_argument_uids:
        pgroups.append(DBDiscussionSession.query(Argument).get(uid).premisesgroup_uid)

    current_argument = DBDiscussionSession.query(Argument).get(arg_id)
    # relation to the arguments premise group
    if attack_type == 'undermine' or attack_type == 'support':  # TODO WHAT IS WITH PGROUPS > 1 ? CAN THIS EVEN HAPPEN IN THE WoR?
        db_premise = DBDiscussionSession.query(Premise).filter_by(
            premisesgroup_uid=current_argument.premisesgroup_uid).first()
        db_statement = DBDiscussionSession.query(Statement).get(db_premise.statement_uid)
        url = _um.get_url_for_choosing_premisegroup(False, False, supportive, db_statement.uid, pgroups)

    # relation to the arguments relation
    elif attack_type == 'undercut' or attack_type == 'overbid':
        url = _um.get_url_for_choosing_premisegroup(False, True, supportive, arg_id, pgroups)

    # relation to the arguments conclusion
    elif attack_type == 'rebut':
        # TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
        is_argument = current_argument.conclusion_uid is not None
        uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
        url = _um.get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

    return url


def get_another_argument_with_same_conclusion(uid, history):
    """
    Returns another supporting/attacking argument with the same conclusion as the given Argument.uid

    :param uid: Argument.uid
    :param history: String
    :return: Argument
    """
    logger('ArgumentsHelper', 'get_another_argument_with_same_conclusion', str(uid))
    db_arg = DBDiscussionSession.query(Argument).get(uid)
    if not db_arg:
        return None

    if db_arg.conclusion_uid is None:
        return None

    # get forbidden uids
    splitted_histoy = history.split('-')
    forbidden_uids = [history.split('/')[2] for history in splitted_histoy if 'reaction' in history] + [uid]

    db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_arg.conclusion_uid,
                                                                  Argument.is_supportive == db_arg.is_supportive,
                                                                  ~Argument.uid.in_(forbidden_uids))).all()
    if len(db_supports) == 0:
        return None

    return db_supports[random.randint(0, len(db_supports) - 1)]