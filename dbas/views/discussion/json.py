from pprint import pprint

from pyramid.view import view_config

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement
from dbas.handler import history as history_handler, user, issue as issue_handler
from dbas.handler.arguments import set_arguments_premises, get_all_infos_about_argument, get_arguments_by_statement_uid
from dbas.handler.issue import set_discussions_properties
from dbas.handler.language import get_language_from_cookie
from dbas.handler.statements import set_position, set_positions_premise, set_correction_of_statement, \
    set_seen_statements, get_logfile_for_statements
from dbas.handler.voting import clear_vote_and_seen_values_of_user
from dbas.helper.query import mark_statement_or_argument
from dbas.lib import relation_mapper, escape_string, get_discussion_language
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.validators.common import valid_language
from dbas.validators.core import validate, has_keywords
from dbas.validators.discussion import valid_any_issue_by_id, valid_issue_not_readonly, valid_conclusion, \
    valid_premisegroups, valid_argument, valid_new_issue, valid_statement_or_argument, valid_issue_by_id, \
    valid_statement
from dbas.validators.user import valid_user, valid_user_optional
from dbas.views.json import __modifiy_discussion_url


@view_config(route_name='get_user_history', renderer='json')
@validate(valid_user)
def get_user_history(request):
    """
    Request the complete user track.

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return history_handler.get_from_database(db_user, ui_locales)


@view_config(route_name='get_all_posted_statements', renderer='json')
@validate(valid_user)
def get_all_posted_statements(request):
    """
    Request for all statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_textversions(db_user, ui_locales).get('statements', [])


@view_config(route_name='get_all_edits', renderer='json')
@validate(valid_user)
def get_all_edits_of_user(request):
    """
    Request for all edits of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_textversions(db_user, ui_locales).get('edits', [])


@view_config(route_name='get_all_marked_arguments', renderer='json')
@validate(valid_user)
def get_all_marked_arguments(request):
    """
    Request for all marked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_marked_elements_of(db_user, True, ui_locales)


@view_config(route_name='get_all_marked_statements', renderer='json')
@validate(valid_user)
def get_all_marked_statements(request):
    """
    Request for all marked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_marked_elements_of(db_user, False, ui_locales)


@view_config(route_name='get_all_argument_clicks', renderer='json')
@validate(valid_user)
def get_all_argument_clicks(request):
    """
    Request for all clicked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_clicked_elements_of(db_user, True, ui_locales)


@view_config(route_name='get_all_statement_clicks', renderer='json')
@validate(valid_user)
def get_all_statement_clicks(request):
    """
    Request for all clicked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_clicked_elements_of(db_user, False, ui_locales)


@view_config(route_name='delete_user_history', renderer='json')
@validate(valid_user)
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_user_history', 'main')
    db_user = request.validated['user']
    return history_handler.delete_in_database(db_user)


@view_config(route_name='delete_statistics', renderer='json')
@validate(valid_user)
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_statistics', 'main')
    db_user = request.validated['user']
    return clear_vote_and_seen_values_of_user(db_user)


@view_config(route_name='set_discussion_properties', renderer='json')
@validate(valid_user, valid_any_issue_by_id, has_keywords(('property', bool), ('value', str)))
def set_discussion_properties(request):
    """
    Set availability, read-only, ... flags in the admin panel.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'request.params: {}'.format(request.json_body))
    _tn = Translator(get_language_from_cookie(request))

    prop = request.validated['property']
    db_user = request.validated['user']
    issue = request.validated['issue']
    value = request.validated['value']
    return set_discussions_properties(db_user, issue, prop, value, _tn)


@view_config(route_name='set_new_start_argument', renderer='json')
@validate(valid_user, valid_issue_not_readonly, has_keywords(('position', str), ('reason', str)))
def set_new_start_argument(request):
    """
    Inserts a new argument as starting point into the database

    :param request: request of the web server
    :return: a status code, if everything was successful
    """
    logger('views', 'request.params: {}'.format(request.json_body))
    reason = request.validated['reason']

    # set the new position
    logger('views', 'set conclusion/position')
    prepared_dict_pos = set_position(request.validated['user'], request.validated['issue'],
                                     request.validated['position'])

    if len(prepared_dict_pos['error']) is 0:
        logger('views', 'set premise/reason')
        prepared_dict_pos = set_positions_premise(request.validated['issue'],
                                                  request.validated['user'],
                                                  DBDiscussionSession.query(Statement).get(
                                                      prepared_dict_pos['statement_uids'][0]),
                                                  [[reason]],
                                                  True,
                                                  request.cookies.get('_HISTORY_'),
                                                  request.mailer)
    __modifiy_discussion_url(prepared_dict_pos)

    return prepared_dict_pos


@view_config(route_name='set_new_start_premise', renderer='json')
@validate(valid_user, valid_issue_not_readonly, valid_conclusion, valid_premisegroups,
          has_keywords(('supportive', bool)))
def set_new_start_premise(request):
    """
    Sets new premise for the start

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    prepared_dict = set_positions_premise(request.validated['issue'],
                                          request.validated['user'],
                                          request.validated['conclusion'],
                                          request.validated['premisegroups'],
                                          request.validated['supportive'],
                                          request.cookies.get('_HISTORY_'),
                                          request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_new_premises_for_argument', renderer='json')
@validate(valid_user, valid_premisegroups, valid_argument(location='json_body', depends_on={valid_issue_not_readonly}),
          has_keywords(('attack_type', str)))
def set_new_premises_for_argument(request):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    prepared_dict = set_arguments_premises(request.validated['issue'],
                                           request.validated['user'],
                                           request.validated['argument'],
                                           request.validated['premisegroups'],
                                           relation_mapper[request.validated['attack_type']],
                                           request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None,
                                           request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_correction_of_statement', renderer='json')
@validate(valid_user, has_keywords(('elements', list)))
def set_correction_of_some_statements(request):
    """
    Sets a new textvalue for a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    elements = request.validated['elements']
    db_user = request.validated['user']
    _tn = Translator(ui_locales)
    return set_correction_of_statement(elements, db_user, _tn)


@view_config(route_name='set_new_issue', renderer='json')
@validate(valid_user, valid_language, valid_new_issue, has_keywords(('is_public', bool), ('is_read_only', bool)))
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    logger('views', 'main {}'.format(request.json_body))
    info = escape_string(request.validated['info'])
    long_info = escape_string(request.validated['long_info'])
    title = escape_string(request.validated['title'])
    lang = request.validated['lang']
    is_public = request.validated['is_public']
    is_read_only = request.validated['is_read_only']

    return issue_handler.set_issue(request.validated['user'], info, long_info, title, lang, is_public, is_read_only)


@view_config(route_name='set_seen_statements', renderer='json')
@validate(valid_user, has_keywords(('uids', list)))
def set_statements_as_seen(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'main {}'.format(request.json_body))
    uids = request.validated['uids']
    return set_seen_statements(uids, request.path, request.validated['user'])


@view_config(route_name='mark_statement_or_argument', renderer='json')
@validate(valid_user, valid_statement_or_argument, has_keywords(('step', str), ('is_supportive', bool),
                                                                ('should_mark', bool)))
def mark_or_unmark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'main {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    arg_or_stmt = request.validated['arg_or_stmt']
    step = request.validated['step']
    is_supportive = request.validated['is_supportive']
    should_mark = request.validated['should_mark']
    history = request.json_body.get('history', '')
    db_user = request.validated['user']
    return mark_statement_or_argument(arg_or_stmt, step, is_supportive, should_mark, history, ui_locales, db_user)


@view_config(route_name='get_logfile_for_statements', renderer='json')
@validate(valid_issue_by_id, has_keywords(('uids', list)))
def get_logfile_for_some_statements(request):
    """
    Returns the changelog of a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    uids = request.validated['uids']
    db_issue = request.validated['issue']
    return get_logfile_for_statements(uids, db_issue.lang, request.application_url)


@view_config(route_name='get_infos_about_argument', renderer='json')
@validate(valid_issue_by_id, valid_language, valid_argument(location='json_body'), valid_user_optional)
def get_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    logger('views', 'main: {}'.format(request.json_body))
    lang = request.validated['lang']
    db_user = request.validated['user']
    db_argument = request.validated['argument']
    return get_all_infos_about_argument(db_argument, request.application_url, db_user, lang)


@view_config(route_name='get_arguments_by_statement_uid', renderer='json')
@validate(valid_any_issue_by_id, valid_statement(location='path'))
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    db_statement = request.validated['statement']
    db_issue = request.validated['issue']
    argument_list = get_arguments_by_statement_uid(db_statement, db_issue)
    for el in argument_list.get('arguments', []):
        el['url'] = '/discuss' + el['url']
    return argument_list
