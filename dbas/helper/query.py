"""
Provides helping function for database querys.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
import dbas.helper.notification as NotificationHelper
import dbas.recommender_system as RecommenderSystem
import dbas.user_management as UserHandler

from sqlalchemy import and_, func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, VoteArgument, VoteStatement, Issue
from dbas.helper.relation import RelationHelper
from dbas.input_validator import Validator
from dbas.lib import escape_string, sql_timestamp_pretty_print, get_text_for_argument_uid, get_text_for_premisesgroup_uid, get_all_attacking_arg_uids_from_history
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

statement_min_length = 10


class QueryHelper:
    """
    Provides several functions for setting new statements or arguments, as well as gettinhg logfiles or many information.
    """

    @staticmethod
    def get_infos_about_argument(uid, lang, mainpage):
        """
        Returns several infos about the argument.

        :param uid: Argument.uid
        :param lang: ui_locales
        :param mainpage: url
        :return: dict()
        """
        return_dict = dict()
        db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid,
                                                                       VoteArgument.is_valid == True,
                                                                       VoteStatement.is_up_vote == True)).all()
        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
        if not db_argument:
            return return_dict

        db_author = DBDiscussionSession.query(User).filter_by(uid=db_argument.author_uid).first()
        return_dict['vote_count']       = str(len(db_votes))
        return_dict['author']           = db_author.public_nickname
        return_dict['timestamp']        = sql_timestamp_pretty_print(db_argument.timestamp, lang)
        text                            = get_text_for_argument_uid(uid, lang)
        return_dict['text']             = text[0:1].upper() + text[1:] + '.'

        supporters = []
        gravatars = dict()
        public_page = dict()
        _um = UserHandler
        for vote in db_votes:
            db_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            supporters.append(db_user.public_nickname)
            gravatars[db_user.public_nickname] = _um.get_public_profile_picture(db_user)
            public_page[db_user.public_nickname] = mainpage + '/user/' + db_user.public_nickname

        return_dict['supporter'] = supporters
        return_dict['gravatars'] = gravatars
        return_dict['public_page'] = public_page

        return return_dict

    @staticmethod
    def process_input_of_start_premises_and_receive_url(request, transaction, premisegroups, conclusion_id, supportive,
                                                        issue, user, for_api, mainpage, lang):
        """
        Inserts the given text in premisegroups as new arguments in dependence of the input parameters and returns a URL for forwarding.

        :param request: request
        :param transaction: Transaction
        :param premisegroups: [String]
        :param conclusion_id: Statement.uid
        :param supportive: Boolean
        :param issue: Issue.uid
        :param user: User.nickname
        :param for_api: Boolean
        :param mainpage: URL
        :param lang: ui_locales
        :return: URL, [Statement.uids], String
        """
        logger('QueryHelper', 'process_input_of_start_premises_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
        _tn = Translator(lang)
        slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
        error = ''
        url = ''
        history = request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None

        # insert all premise groups into our database
        # all new arguments are collected in a list
        new_argument_uids = []
        new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
        for group in premisegroups:  # premise groups is a list of lists
            new_argument, statement_uids = QueryHelper.__create_argument_by_raw_input(transaction, user, group, conclusion_id, supportive, issue)
            if not isinstance(new_argument, Argument):  # break on error
                error = _tn.get(_tn.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_tn.minLength) + ': ' + str(statement_min_length) + ')'
                return -1, None, error

            new_argument_uids.append(new_argument.uid)
            if for_api:
                new_statement_uids.append(statement_uids)

        # #arguments=0: empty input
        # #arguments=1: deliver new url
        # #arguments>1: deliver url where the user has to choose between her inputs
        _um = UrlManager(mainpage, slug, for_api, history)
        if len(new_argument_uids) == 0:
            error = QueryHelper.__get_error_for_empty_argument_list(_tn)

        elif len(new_argument_uids) == 1:
            url = QueryHelper.__get_url_for_new_argument(new_argument_uids, history, lang, _um)

        else:
            pgroups = []
            for arg_uid in new_argument_uids:
                pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first().premisesgroup_uid)
            url = _um.get_url_for_choosing_premisegroup(False, False, supportive, conclusion_id, pgroups)

        # send notifications and mails
        if len(new_argument_uids) > 0:
            url = _um.get_url_for_justifying_statement(False, conclusion_id, 't' if supportive else 'f')
            NotificationHelper.send_add_text_notification(url, conclusion_id, user, request, transaction)

        return url, new_statement_uids, error

    @staticmethod
    def process_input_of_premises_for_arguments_and_receive_url(request, transaction, arg_id, attack_type, premisegroups,
                                                                issue, user, for_api, mainpage, lang):
        """
        Inserts the given text in premisegroups as new arguments in dependence of the input paramters and returns a URL for forwarding.

        .. note::

            Optimize the "for_api" part

        :param request: request
        :param transaction: transaction
        :param arg_id: Argument.uid
        :param attack_type: String
        :param premisegroups: [Strings]
        :param issue: Issue.uid
        :param user: User.nickname
        :param for_api: Boolean
        :param mainpage: URL
        :param lang: ui_locales
        :return: URL, [Statement.uids], String
        """
        logger('QueryHelper', 'process_input_of_premises_for_arguments_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
        _tn = Translator(lang)
        slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
        error = ''
        history = request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None
        supportive = attack_type == 'support' or attack_type == 'overbid'

        # insert all premise groups into our database
        # all new arguments are collected in a list
        new_argument_uids = []
        for group in premisegroups:  # premise groups is a list of lists
            new_argument = QueryHelper.__insert_new_premises_for_argument(group, attack_type, arg_id, issue, user, transaction)
            if not isinstance(new_argument, Argument):  # break on error
                error = _tn.get(_tn.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_tn.minLength) + ': ' + str(statement_min_length) + ')'
                return -1, None, error

            new_argument_uids.append(new_argument.uid)

        statement_uids = []
        if for_api:
            # @OPTIMIZE
            # Query all recently stored premises (internally: statements) and collect their ids
            # This is a bad workaround, let's just think about it in future.
            for uid in new_argument_uids:
                current_pgroup = DBDiscussionSession.query(Argument).filter_by(uid=uid).first().premisesgroup_uid
                current_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_pgroup).all()
                for premise in current_premises:
                    statement_uids.append(premise.statement_uid)

        # #arguments=0: empty input
        # #arguments=1: deliver new url
        # #arguments>1: deliver url where the user has to choose between her inputs
        _um = url = UrlManager(mainpage, slug, for_api, history)
        if len(new_argument_uids) == 0:
            error = QueryHelper.__get_error_for_empty_argument_list(_tn)

        elif len(new_argument_uids) == 1:
            url = QueryHelper.__get_url_for_new_argument(new_argument_uids, history, lang, _um)

        else:
            pgroups = []
            for uid in new_argument_uids:
                pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=uid).first().premisesgroup_uid)

            current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_id).first()
            # relation to the arguments premise group
            if attack_type == 'undermine' or attack_type == 'support':  # TODO WHAT IS WITH PGROUPS > 1 ? CAN THIS EVEN HAPPEN IN THE WoR?
                db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).first()
                db_statement = DBDiscussionSession.query(Statement).filter_by(uid=db_premise.statement_uid).first()
                url = _um.get_url_for_choosing_premisegroup(False, False, supportive, db_statement.uid, pgroups)

            # relation to the arguments relation
            elif attack_type == 'undercut' or attack_type == 'overbid':
                url = _um.get_url_for_choosing_premisegroup(False, True, supportive, arg_id, pgroups)

            # relation to the arguments conclusion
            elif attack_type == 'rebut':
                # TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
                is_argument = current_argument.conclusion_uid is not None
                uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
                url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

        # send notifications and mails
        if len(new_argument_uids) > 0:
            new_uid = new_argument_uids[0] if len(new_argument_uids) == 1 else random.choice(new_argument_uids)   # TODO eliminate random
            attack = Validator.get_relation_between_arguments(arg_id, new_uid)

            tmp_url = _um.get_url_for_reaction_on_argument(False, arg_id, attack, new_uid)

            NotificationHelper.send_add_argument_notification(tmp_url, arg_id, user, request, transaction)

        return url, statement_uids, error

    @staticmethod
    def __get_error_for_empty_argument_list(_tn):
        """

        :param _tn:
        :return:
        """
        return _tn.get(_tn.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_tn.minLength) + ': ' + str(statement_min_length) + ')'

    @staticmethod
    def __get_url_for_new_argument(new_argument_uids, history, lang, urlmanager):
        new_argument_uid = random.choice(new_argument_uids)  # TODO eliminate random
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(history)
        arg_id_sys, attack = RecommenderSystem.get_attack_for_argument(new_argument_uid, lang, restriction_on_arg_uids=attacking_arg_uids)
        if arg_id_sys == 0:
            attack = 'end'
        url = urlmanager.get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
        return url

    @staticmethod
    def correct_statement(transaction, user, uid, corrected_text, path, request):
        """
        Corrects a statement

        :param transaction: transaction current transaction
        :param user: User.nickname requesting user
        :param uid: requested statement uid
        :param corrected_text: new text
        :param path: current path
        :param request: current request
        :return: True
        """
        logger('QueryHelper', 'correct_statement', 'def ' + str(uid))

        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

        if not db_user:
            return -1

        while corrected_text.endswith(('.', '?', '!')):
            corrected_text = corrected_text[:-1]

        # duplicate check
        return_dict = dict()
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
        db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).all()

        # duplicate or not?
        if db_textversion:
            textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=db_textversion[0].uid).first()
        else:
            textversion = TextVersion(content=corrected_text, author=db_user.uid)
            textversion.set_statement(db_statement.uid)
            DBDiscussionSession.add(textversion)
            DBDiscussionSession.flush()

        NotificationHelper.send_edit_text_notification(db_user, textversion, path, request)

        db_statement.set_textversion(textversion.uid)
        transaction.commit()

        return_dict['uid'] = uid
        return_dict['text'] = corrected_text
        return return_dict

    @staticmethod
    def insert_as_statements(transaction, text_list, user, issue, is_start=False):
        """
        Inserts the given texts as statements and returns the uids

        :param transaction: transaction
        :param text_list: [String]
        :param user: User.nickname
        :param issue: Issue
        :param is_start: Boolean
        :return: [Statement]
        """
        statements = []
        if isinstance(text_list, list):
            for text in text_list:
                if len(text) < statement_min_length:
                    return -1
                else:
                    new_statement, is_duplicate = QueryHelper.__set_statement(transaction, text, user, is_start, issue)
                    statements.append(new_statement)
        else:
            if len(text_list) < statement_min_length:
                return -1
            else:
                new_statement, is_duplicate = QueryHelper.__set_statement(transaction, text_list, user, is_start, issue)
                statements.append(new_statement)
        return statements

    @staticmethod
    def get_every_attack_for_island_view(arg_uid, lang):
        """
        Select and returns every argument with an relation to the given Argument.uid

        :param arg_uid: Argument.uid
        :param lang: ui_locales
        :return: dict()
        """
        logger('QueryHelper', 'get_every_attack_for_island_view', 'def with arg_uid: ' + str(arg_uid))
        return_dict = {}
        _t = Translator(lang)
        _rh = RelationHelper(arg_uid, lang)

        undermine = _rh.get_undermines_for_argument_uid()
        support = _rh.get_supports_for_argument_uid()
        undercut = _rh.get_undercuts_for_argument_uid()
        # overbid = _rh.get_overbids_for_argument_uid()
        rebut = _rh.get_rebuts_for_argument_uid()

        undermine = undermine if undermine else [{'id': 0, 'text': _t.get(_t.no_entry)}]
        support = support if support else [{'id': 0, 'text': _t.get(_t.no_entry)}]
        undercut = undercut if undercut else [{'id': 0, 'text': _t.get(_t.no_entry)}]
        # overbid = overbid if overbid else [{'id': 0, 'text': _t.get(_t.no_entry)}]
        rebut = rebut if rebut else [{'id': 0, 'text': _t.get(_t.no_entry)}]

        return_dict.update({'undermine': undermine})
        return_dict.update({'support': support})
        return_dict.update({'undercut': undercut})
        # return_dict.update({'overbid': overbid})
        return_dict.update({'rebut': rebut})

        # pretty pring
        for dict in return_dict:
            for entry in return_dict[dict]:
                has_entry = False if entry['id'] == 0 or lang == 'de' else True
                entry['text'] = (_t.get(_t.because) + ' ' if has_entry else '') + entry['text']

        logger('QueryHelper', 'get_every_attack_for_island_view', 'summary: ' +
               str(len(undermine)) + ' undermines, ' +
               str(len(support)) + ' supports, ' +
               str(len(undercut)) + ' undercuts, ' +
               # str(len(overbid)) + ' overbids, ' +
               str(len(rebut)) + ' rebuts')

        return return_dict

    @staticmethod
    def get_logfile_for_statement(uid, lang, mainpage):
        """
        Returns the logfile for the given statement uid

        :param uid: requested statement uid
        :param lang: ui_locales ui_locales
        :param mainpage: URL
        :return: dictionary with the logfile-rows
        """
        logger('QueryHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).all()

        return_dict = dict()
        content_dict = dict()
        # add all corrections
        for index, versions in enumerate(db_textversions):
            db_author = DBDiscussionSession.query(User).filter_by(uid=versions.author_uid).first()
            corr_dict = dict()
            corr_dict['uid'] = str(versions.uid)
            corr_dict['author'] = str(db_author.public_nickname)
            corr_dict['author_url'] = mainpage + '/user/' + str(db_author.public_nickname)
            corr_dict['author_gravatar'] = UserHandler.get_public_profile_picture(db_author, 20)
            corr_dict['date'] = sql_timestamp_pretty_print(versions.timestamp, lang)
            corr_dict['text'] = str(versions.content)
            content_dict[str(index)] = corr_dict
        return_dict['content'] = content_dict

        return return_dict

    @staticmethod
    def __insert_new_premises_for_argument(text, current_attack, arg_uid, issue, user, transaction):
        """

        :param text: String
        :param current_attack: String
        :param arg_uid: Argument.uid
        :param issue: Issue
        :param user: User.nickname
        :param transaction: transaction
        :return:
        """
        logger('QueryHelper', '__insert_new_premises_for_argument', 'def')
        _rh = RelationHelper()

        statements = QueryHelper.insert_as_statements(transaction, text, user, issue)
        if statements == -1:
            return -1

        # set the new statements as premise group and get current user as well as current argument
        new_pgroup_uid = QueryHelper.__set_statements_as_new_premisegroup(statements, user, issue)
        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
        current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()

        new_argument = None
        if current_attack == 'undermine':
            new_argument = _rh.set_new_undermine_or_support(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

        elif current_attack == 'support':
            new_argument, duplicate = _rh.set_new_support(transaction, new_pgroup_uid, current_argument, db_user, issue)

        elif current_attack == 'undercut' or current_attack == 'overbid':
            new_argument, duplicate = _rh.set_new_undercut_or_overbid(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

        elif current_attack == 'rebut':
            new_argument, duplicate = _rh.set_new_rebut(transaction, new_pgroup_uid, current_argument, db_user, issue)

        return new_argument

    @staticmethod
    def __set_statement(transaction, statement, user, is_start, issue):
        """
        Saves statement for user

        :param transaction: transaction current transaction
        :param statement: given statement
        :param user: User.nickname given user
        :param is_start: if it is a start statement
        :param issue: Issue
        :return: Statement, is_duplicate or -1, False on error
        """
        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
        logger('QueryHelper', 'set_statement', 'user: ' + str(user) + ', user_id: ' + str(db_user.uid) +
               ', statement: ' + str(statement) + ', issue: ' + str(issue))

        # escaping
        statement = escape_string(statement)

        # check for dot at the end
        if not statement.endswith(('.', '?', '!')):
            statement += '.'
        if statement.lower().startswith('because '):
            statement = statement[8:]

        # check, if the statement already exists
        db_duplicate = DBDiscussionSession.query(TextVersion).filter(func.lower(TextVersion.content) == statement.lower()).first()
        if db_duplicate:
            db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == db_duplicate.uid,
                                                                            Statement.issue_uid == issue)).first()
            return db_statement, True

        # add textversion
        textversion = TextVersion(content=statement, author=db_user.uid)
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.flush()

        # add statement
        statement = Statement(textversion=textversion.uid, is_position=is_start, issue=issue)
        DBDiscussionSession.add(statement)
        DBDiscussionSession.flush()

        # get new statement
        new_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == textversion.uid,
                                                                         Statement.issue_uid == issue)).order_by(Statement.uid.desc()).first()
        textversion.set_statement(new_statement.uid)

        transaction.commit()

        return new_statement, False

    @staticmethod
    def __get_attack_or_support_for_justification_of_argument_uid(argument_uid, is_supportive, lang):
        """

        :param argument_uid: Argument.uid
        :param is_supportive: Boolean
        :param lang: ui_locales
        :return:
        """
        return_array = []
        logger('QueryHelper', '__get_attack_or_support_for_justification_of_argument_uid',
               'db_undercut against Argument.argument_uid==' + str(argument_uid))
        db_related_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
                                                                               Argument.argument_uid == argument_uid)).all()
        given_relations = set()
        index = 0

        if not db_related_arguments:
            return None

        for relation in db_related_arguments:
            if relation.premisesgroup_uid not in given_relations:
                given_relations.add(relation.premisesgroup_uid)
                tmp_dict = dict()
                tmp_dict['id'] = relation.uid
                tmp_dict['text'], trash = get_text_for_premisesgroup_uid(relation.premisesgroup_uid, lang)
                return_array.append(tmp_dict)
                index += 1
        return return_array

    @staticmethod
    def __create_argument_by_raw_input(transaction, user, text, conclusion_id, is_supportive, issue):
        """

        :param transaction: transaction
        :param user: User.nickname
        :param text: String
        :param conclusion_id:
        :param is_supportive: Boolean
        :param issue: Issue
        :return:
        """
        logger('QueryHelper', 'set_premises_as_group_for_conclusion', 'main with text ' + str(text))
        # current conclusion
        db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                         Statement.issue_uid == issue)).first()
        statements = QueryHelper.insert_as_statements(transaction, text, user, issue)
        if statements == -1:
            return -1, None

        statement_uids = [s.uid for s in statements]

        # second, set the new statements as premisegroup
        new_premisegroup_uid = QueryHelper.__set_statements_as_new_premisegroup(statements, user, issue)

        # third, insert the argument
        new_argument = QueryHelper.__create_argument_by_uids(transaction, user, new_premisegroup_uid, db_conclusion.uid, None, is_supportive, issue)

        transaction.commit()
        return new_argument, statement_uids

    @staticmethod
    def __create_argument_by_uids(transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
        """

        :param transaction: transaction
        :param user: User.nickname
        :param premisegroup_uid: PremseGroup.uid
        :param conclusion_uid: Statement.uid
        :param argument_uid: Argument.uid
        :param is_supportive: Boolean
        :param issue: Issue.uid
        :return:
        """
        logger('QueryHelper', '__create_argument_by_uids', 'main with user: ' + str(user) +
               ', premisegroup_uid: ' + str(premisegroup_uid) +
               ', conclusion_uid: ' + str(conclusion_uid) +
               ', argument_uid: ' + str(argument_uid) +
               ', is_supportive: ' + str(is_supportive) +
               ', issue: ' + str(issue))

        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
        new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.issue_uid == issue)).first()
        if not new_argument:
            new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid,
                                    conclusion=conclusion_uid, issue=issue)
            new_argument.conclusions_argument(argument_uid)

            DBDiscussionSession.add(new_argument)
            DBDiscussionSession.flush()

            new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                           Argument.is_supportive == is_supportive,
                                                                           Argument.author_uid == db_user.uid,
                                                                           Argument.conclusion_uid == conclusion_uid,
                                                                           Argument.argument_uid == argument_uid,
                                                                           Argument.issue_uid == issue)).first()
        transaction.commit()
        if new_argument:
            logger('QueryHelper', '__create_argument_by_uids', 'argument was inserted')
            return new_argument
        else:
            logger('QueryHelper', '__create_argument_by_uids', 'argument was not inserted')
            return None

    @staticmethod
    def __set_statements_as_new_premisegroup(statements, user, issue):
        """

        :param statements:
        :param user: User.nickname
        :param issue: Issue
        :return:
        """
        logger('QueryHelper', '__set_statements_as_new_premisegroup', 'user: ' + str(user) +
               ', statement: ' + str(statements) + ', issue: ' + str(issue))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

        # check for duplicate
        all_groups = []
        for statement in statements:
            # get the premise
            db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
            if db_premise:
                # getting all groups, where the premise is member
                db_premisegroup = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_premise.premisesgroup_uid).all()
                groups = set()
                for group in db_premisegroup:
                    groups.add(group.premisesgroup_uid)
                all_groups.append(groups)
        # if every set in this array has one common member, they are all in the same group
        if len(all_groups) > 0:
            intersec = set.intersection(*all_groups)
            for group in intersec:
                db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group).all()
                if len(db_premise) == len(statements):
                    return group

        premise_group = PremiseGroup(author=db_user.uid)
        DBDiscussionSession.add(premise_group)
        DBDiscussionSession.flush()

        premise_list = []
        for statement in statements:
            premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, is_negated=False, author=db_user.uid, issue=issue)
            premise_list.append(premise)

        DBDiscussionSession.add_all(premise_list)
        DBDiscussionSession.flush()

        db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

        return db_premisegroup.uid