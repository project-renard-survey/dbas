#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ClickedStatement, ClickedArgument, User, MarkedArgument, MarkedStatement
from dbas.lib import get_author_data, Relations
from dbas.strings.lib import start_with_capital, start_with_small
from .keywords import Keywords as _
from .translator import Translator

nick_of_anonymous_user = 'anonymous'

tag_type = 'span'
start_attack = '<{} data-argumentation-type="attack">'.format(tag_type)
start_argument = '<{} data-argumentation-type="argument">'.format(tag_type)
start_position = '<{} data-argumentation-type="position">'.format(tag_type)
start_content = '<{} class="triangle-content-text">'.format(tag_type)
start_pro = '<{} data-attitude="pro">'.format(tag_type)
start_con = '<{} data-attitude="con">'.format(tag_type)
start_tag = '<{}>'.format(tag_type)
end_tag = '</{}>'.format(tag_type)


def get_text_for_add_premise_container(lang, confrontation, premise, attack_type, conclusion, is_supportive):
    """
    Based on the users reaction, text will be build. This text can be used for the container where users can
    add their statements

    :param lang: ui_locales
    :param confrontation: chosen confrontation
    :param premise: current premise
    :param attack_type: type of the attack
    :param conclusion: current conclusion
    :param is_supportive: boolean
    :return: string
    """
    _t = Translator(lang)

    while premise[-1] in ['.', ' ']:
        premise = premise[:-1]

    while conclusion[-1] in ['.', ' ']:
        conclusion = premise[:-1]

    confrontation = start_with_capital(confrontation)

    # different cases
    if attack_type == Relations.UNDERMINE:
        return '{} {} ...'.format(_t.get(_.itIsFalseThat), premise)

    elif attack_type == Relations.SUPPORT:
        intro = _t.get(_.itIsFalseThat)
        outro = _t.get(_.doesNotHold)
        if is_supportive:
            intro = _t.get(_.itIsTrueThat)
            outro = _t.get(_.hold)
        return '{} {} {} ...'.format(intro, conclusion, outro)

    elif attack_type == Relations.UNDERCUT:
        return '{}, {} ...'.format(confrontation, _t.get(_.butIDoNotBelieveCounterFor).format(conclusion))

    elif attack_type == Relations.REBUT:
        mid = _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
        return '{} {} {} ...'.format(confrontation, mid, conclusion)

    else:
        return ''


def get_header_for_users_confrontation_response(db_argument, lang, premise, attack_type, conclusion, start_lower_case,
                                                is_supportive, is_logged_in, redirect_from_jump=False):
    """
    Based on the users reaction, text will be build. This text can be used for the speech bubbles where users
    justify an argument they have chosen.

    :param db_argument: Argument
    :param lang: ui_locales
    :param premise: current premise
    :param attack_type: type of the attack
    :param conclusion: current conclusion
    :param start_lower_case: boolean
    :param is_supportive: boolean
    :param is_logged_in: boolean
    :param redirect_from_jump: boolean
    :return: string
    """
    _t = Translator(lang)

    if premise[-1] == '.':
        premise = premise[:-1]

    if conclusion[-1] == '.':
        conclusion = conclusion[:-1]

    # pretty print
    r = _t.get(_.right)[0:1].upper()
    f = _t.get(_.itIsFalseThat)[0:1].upper()
    t = _t.get(_.itIsTrueThat)[0:1].upper()
    if start_lower_case:
        r = _t.get(_.right)[0:1].lower()
        f = _t.get(_.itIsFalseThat)[0:1].lower()
        t = _t.get(_.itIsTrueThat)[0:1].lower()

    r += _t.get(_.right)[1:] + ', '
    f += _t.get(_.itIsFalseThat)[1:]
    t += _t.get(_.itIsTrueThat)[1:]

    if lang == 'de':
        r += start_with_small(_t.get(_.itIsTrueThat)) + ' '
        f = _t.get(_.wrong) + ', ' + start_with_small(_t.get(_.itIsFalseThat)) + ' '

    if redirect_from_jump:
        r = _t.get(_.maybeItIsTrueThat) + ' '

    # different cases
    user_msg = __get_user_msg_for_users_confrontation_response(db_argument, attack_type, premise, conclusion, f, t, r,
                                                               is_supportive, _t)
    if not user_msg:
        user_msg = ''

    # is logged in?
    if is_logged_in:
        return user_msg, _t.get(_.canYouGiveAReasonForThat)
    else:
        return user_msg, ''


def __get_user_msg_for_users_confrontation_response(db_argument, attack_type, premise, conclusion, itisfalsethat,
                                                    itistruethat, right, is_supportive, _t):
    """
    Builds a string based on the attack type to confront the user

    :param db_argument: Argument
    :param attack_type: String
    :param premise: String
    :param conclusion: String
    :param itisfalsethat: String
    :param itistruethat: String
    :param right: String
    :param is_supportive: Boolean
    :param _t: Translator
    :return: String
    """
    # different cases
    if attack_type == Relations.UNDERMINE:
        return __get_user_msg_for_users_undermine_response(premise, _t.get(_.that))

    if attack_type == Relations.SUPPORT:
        return __get_user_msg_for_users_support_response(conclusion, itistruethat, itisfalsethat, is_supportive, _t)

    if attack_type == Relations.UNDERCUT:
        return __get_user_msg_for_users_undercut_response(db_argument, premise, conclusion, right, _t)

    if attack_type == Relations.REBUT:
        return __get_user_msg_for_users_rebut_response(premise, conclusion, right, is_supportive, _t)


def __get_user_msg_for_users_undermine_response(premise, that):
    """
    Simple text for an undermine

    :param premise: String
    :param that: String
    :return: String
    """
    return '{} {}{}{}'.format(that, '{}', premise, '{}')


def __get_user_msg_for_users_support_response(conclusion, itistruethat, itisfalsethat, is_supportive, _t):
    """
    Simple text for an support

    :param conclusion: String
    :param itistruethat: String
    :param itisfalsethat: String
    :param is_supportive: String
    :param _t: Translator
    :return: String
    """
    if is_supportive:
        intro = itistruethat
        outro = _t.get(_.hold)
    else:
        intro = itisfalsethat
        outro = _t.get(_.doesNotHold)

    return '{}{} {} {}{}.'.format('{}', intro, conclusion, outro, '{}')


def __get_user_msg_for_users_undercut_response(db_argument, premise, conclusion, right, _t):
    """
    Simple text for the undercut

    :param db_argument: Argument
    :param premise: String
    :param conclusion: String
    :param right: String
    :param _t: Translator
    :return:
    """
    tmp = None
    if db_argument.conclusion_uid is None and _t.get_lang() == 'de':
        # undercutting an undercut
        start_text = _t.get(_.itIsTrueThatAnonymous)
        if conclusion.lower().startswith(start_text.lower()):
            conclusion = conclusion[len(start_text):]
            tmp = _t.get(_.butThisDoesNotRejectArgument)

    if tmp is None:
        tmp = _t.get(_.butIDoNotBelieveArgumentFor if db_argument.is_supportive else _.butIDoNotBelieveCounterFor)
    tmp = tmp.format(conclusion)

    return '{}{}. {}{}{}'.format(right, premise, '{}', tmp, '{}')


def __get_user_msg_for_users_rebut_response(premise, conclusion, right, is_supportive, _t):
    """
    Simple text for the rebut

    :param premise: String
    :param conclusion: String
    :param right: String
    :param is_supportive:
    :param _t: Translator
    :return: String
    """
    if is_supportive:
        intro = _t.get(_.iAcceptCounterThat)
        mid = _t.get(_.howeverIHaveMuchStrongerArgumentRejectingThat)
    else:
        intro = _t.get(_.iAcceptArgumentThat)
        mid = _t.get(_.howeverIHaveMuchStrongerArgumentAcceptingThat)

    return '{}{}{}, {} {}. {} {}.{}'.format('{}', right, premise, intro, conclusion, mid, conclusion, '{}')


def get_relation_text_dict_without_substitution(lang, with_no_opinion_text, premise, conclusion, is_dont_know=False):
    """
    Returns the four different reaction possibilities without any replacement based on the gender of the confrontation

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param premise: String
    :param conclusion: String
    :param is_dont_know: Boolean
    :return: dict()
    """
    return __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know)


def get_relation_text_dict_with_substitution(lang, with_no_opinion_text, is_dont_know=False, attack_type=None,
                                             gender=''):
    """
    Returns the four different reaction possibilities with replacements based on the gender of the confrontation

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param is_dont_know: Boolean
    :param attack_type: String
    :param gender: String
    :return: dict()
    """
    _t = Translator(lang)

    assertion = _t.get(_.theirAssertion)
    reason = _t.get(_.theirReason)
    statement = _t.get(_.theirStatement)
    position = _t.get(_.theirPosition)
    opinion = _t.get(_.opinion)
    if gender == 'f':
        assertion = _t.get(_.herAssertion)
        reason = _t.get(_.herReason)
        statement = _t.get(_.herStatement)
        position = _t.get(_.herPosition)
        opinion = _t.get(_.opinion_her)
    elif gender == 'm':
        assertion = _t.get(_.hisAssertion)
        reason = _t.get(_.hisReason)
        statement = _t.get(_.hisStatement)
        position = _t.get(_.hisPosition)
        opinion = _t.get(_.opinion_his)

    premise = statement
    if lang == 'de':
        if is_dont_know:
            premise = assertion

        conclusion = assertion
        if is_dont_know:
            conclusion = reason

    else:
        conclusion = opinion
        if not is_dont_know:
            if attack_type == Relations.UNDERMINE or attack_type == Relations.REBUT:
                conclusion = position
            else:
                conclusion = _t.get(_.myArgument)

    return __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know)


def __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know=False):
    """
    Text of the different reaction types for an given argument

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param premise: String
    :param conclusion: String
    :param is_dont_know: Boolean
    :return: dict()
    """
    _t = Translator(lang)

    premise = start_attack + premise + end_tag
    conclusion = start_argument + conclusion + end_tag

    ret_dict = dict()

    if with_no_opinion_text:
        ret_dict['step_back_text'] = _t.get(_.goStepBack) + '. (' + _t.get(_.noOtherAttack) + ')'
        ret_dict['no_opinion_text'] = _t.get(_.showMeAnotherArgument) + '.'

    ret_dict['undermine_text'] = _t.get(_.reaction_text_undermine).format(premise)

    ret_dict['support_text'] = _t.get(_.reaction_text_support).format(premise)

    ret_dict['undercut_text'] = _t.get(_.reaction_text_undercut).format(premise, conclusion)
    if is_dont_know:
        tmp = start_argument + _t.get(_.reason) + end_tag
        ret_dict['undercut_text'] = _t.get(_.reaction_text_undercut_for_dont_know).format(premise, tmp)

    conclusion_user = start_position + _t.get(_.myPosition) + end_tag
    ret_dict['rebut_text'] = _t.get(_.reaction_text_rebut).format(premise, conclusion, conclusion_user)
    if is_dont_know:
        ret_dict['rebut_text'] = _t.get(_.reaction_text_rebut_for_dont_know).format(conclusion)

    return ret_dict


def get_jump_to_argument_text_list(lang):
    """
    Returns answer set for the jumping step

    :param lang: ui_locales
    :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong)
             Premise does not lead to the conclusion, both hold]
    """
    _t = Translator(lang)

    premise = start_attack + _t.get(_.reason) + end_tag
    conclusion = start_argument + _t.get(_.assertion) + end_tag

    answers = list()

    answers.append(_t.get(_.jumpAnswer0).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer1).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer2).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer3).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer4).format(premise))

    return answers


def get_support_to_argument_text_list(lang):
    """
    Returns answer set for the supporting step

    :param lang: ui_locales
    :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong)
             Premise does not lead to the conclusion, both hold]
    """
    _t = Translator(lang)

    premise = start_attack + _t.get(_.reason) + end_tag
    conclusion = start_argument + _t.get(_.assertion) + end_tag

    answers = list()

    answers.append(_t.get(_.supportAnswer0).format(premise))
    answers.append(_t.get(_.supportAnswer3).format(premise))
    answers.append(_t.get(_.supportAnswer1).format(premise))
    answers.append(_t.get(_.supportAnswer2).format(premise, conclusion))

    return answers


def get_text_for_confrontation(lang, nickname, premise, conclusion, sys_conclusion, supportive, attack,
                               confrontation, reply_for_argument, user_is_attacking, user_arg, sys_arg,
                               color_html=True):
    """
    Text for the confrontation of the system

    :param main_page: main_page
    :param lang: ui_locales
    :param nickname: nickname
    :param premise: String
    :param conclusion: String
    :param sys_conclusion: String
    :param supportive: String
    :param attack: String
    :param confrontation: String
    :param reply_for_argument: Boolean
    :param user_is_attacking: Boolean
    :param user_arg: Argument
    :param sys_arg: Argument
    :param color_html: Boolean
    :return: String
    """
    my_start_argument = ''
    my_end_tag = ''

    if color_html:
        my_start_attack = start_attack
        my_start_argument = start_argument
        my_end_tag = end_tag
        confrontation = my_start_attack + confrontation + my_end_tag
        conclusion = my_start_argument + conclusion + my_end_tag
        if attack == Relations.UNDERMINE:
            premise = my_start_argument + premise + my_end_tag
        sys_conclusion = my_start_argument + sys_conclusion + my_end_tag

    # build some confrontation text
    if attack == Relations.UNDERMINE:
        confrontation_text, gender = __get_confrontation_text_for_undermine(nickname, premise, lang, sys_arg,
                                                                            my_start_argument, my_end_tag,
                                                                            confrontation)

    elif attack == Relations.UNDERCUT:
        confrontation_text, gender = __get_confrontation_text_for_undercut(nickname, lang,
                                                                           premise, conclusion, confrontation,
                                                                           supportive, sys_arg)

    elif attack == Relations.REBUT:
        confrontation_text, gender = __get_confrontation_text_for_rebut(lang, nickname, reply_for_argument,
                                                                        user_arg, user_is_attacking, sys_conclusion,
                                                                        confrontation, premise, conclusion,
                                                                        my_start_argument, sys_arg)
    else:
        return '', ''

    _t = Translator(lang)
    question = '{}.<br><br>{}?{}'.format(start_tag, _t.get(_.whatDoYouThinkAboutThat), end_tag)
    sys_text = confrontation_text + question
    return sys_text, gender


def get_text_for_support(db_arg, argument_text, nickname, _t):
    """
    Returns text for the system bubble during the support step

    :param db_arg: Argument
    :param argument_text: string
    :param nickname: User.nickname
    :param _t: translator
    :return: string
    """
    data = get_name_link_of_arguments_author(db_arg, nickname)
    intro = _t.get(_.goodPointAndOtherParticipantsIsInterestedToo).format(start_tag, end_tag, argument_text)
    if data['is_valid']:
        intro = _t.get(_.goodPointAndUserIsInterestedTooF)
        if data['gender'] == 'm':
            intro = _t.get(_.goodPointAndUserIsInterestedTooM)
        intro = intro.format(start_tag, end_tag, data['link'], start_tag, end_tag, argument_text)

    question = '<br><br>{}?'.format(_t.get(_.whatDoYouThinkAboutThat))

    return intro + question


def get_text_for_edit_text_message(lang, nickname, orginal, edit, url, for_html=True):
    """
    Returns text for the editing an statement

    :param lang: Language.ui_locales
    :param nickname: User.nickname
    :param orginal:
    :param edit:
    :param url: String
    :param for_html: Boolean
    :return:
    """
    _t = Translator(lang)
    if for_html:
        return _t.get(_.editTextMessageForHtml).format(nickname, orginal, edit, url, url)
    else:
        return _t.get(_.editTextMessage).format(nickname, orginal, edit, url)


def get_text_for_add_text_message(nickname, lang, url, for_html=True):
    """
    Returns text for the adding an statement

    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param url: String
    :param for_html: Boolean
    :return:
    """
    return __get_text_for_add_something(nickname, lang, url, _.statementAddedMessageContent, for_html)


def get_text_for_add_argument_message(nickname, lang, url, for_html=True):
    """
    Returns text for the adding an argument

    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param url: String
    :param for_html: Boolean
    :return:
    """
    return __get_text_for_add_something(nickname, lang, url, _.argumentAddedMessageContent, for_html)


def __get_text_for_add_something(nickname, lang, url, keyword, for_html=True):
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    intro = _t.get(keyword).format(nickname)
    w = start_with_capital(_t.get(_.where))
    if for_html:
        url = '<a href="{}">{}</a>'.format(url, url)

    return '{}{}{}: {}'.format(intro, nl, w, url)


def __get_confrontation_text_for_undermine(nickname, premise, lang, system_argument, my_start_argument,
                                           my_end_tag, confrontation):
    """
    Returns the system bubble text for an undermine

    :param nickname: User.nickname
    :param premise: String
    :param lang: Language
    :param system_argument: String
    :param my_start_argument: String
    :param my_end_tag: String
    :param confrontation: String
    :return:
    """
    _t = Translator(lang)

    move_end_tag = False
    if tag_type not in premise:
        premise = start_tag + premise + end_tag
    if tag_type not in confrontation:
        confrontation = start_tag + confrontation + end_tag
        move_end_tag = True

    data = get_name_link_of_arguments_author(system_argument, nickname)
    if data['is_valid']:
        intro = '{} {}{}'.format(data['link'], start_content, _t.get(_.thinksThat))
    else:
        intro = start_content + _t.get(_.otherParticipantsThinkThat)

    pro_con_tag = start_con
    hold_it = _t.get(_.doesNotHold)
    if system_argument.is_supportive:
        pro_con_tag = start_pro
        hold_it = _t.get(_.hold)

    outro = my_end_tag if move_end_tag else ''

    confrontation_text = '{}{} {}{}{} {}{}{}{}{}{}, {}{} {}{}'.format(intro, end_tag, premise, pro_con_tag, start_tag,
                                                                      my_start_argument, hold_it, my_end_tag, end_tag,
                                                                      my_end_tag, start_tag,
                                                                      _t.get(_.because).lower(), end_tag,
                                                                      confrontation, outro)

    return confrontation_text, data['gender'] if data['is_valid'] else ''


def __get_confrontation_text_for_undercut(nickname, lang, premise, conclusion, confrontation, supportive,
                                          system_argument):
    """
    Returns the system bubble text for an undercut

    :param nickname: User.nickname
    :param lang: Language
    :param premise: String
    :param conclusion: String
    :param confrontation: String
    :param supportive: Boolean
    :param system_argument: String
    :return:
    """
    _t = Translator(lang)

    data = get_name_link_of_arguments_author(system_argument, nickname)

    if data['is_valid']:
        intro = data['link'] + ' ' + start_content + _t.get(_.agreesThat)
        gender_think = _t.get(_.theyThink)
        if data['is_valid']:
            gender_think = __translation_based_on_gender(_t, _.heThinks, _.sheThinks, data['gender'])
    else:
        intro = start_content + _t.get(_.otherParticipantsDontHaveOpinion)
        gender_think = _t.get(_.theyThinkThat)

    if supportive:
        bind = _t.get(_.butTheyDoNotBelieveArgument)
        if data['is_valid']:
            bind = __translation_based_on_gender(_t, _.butHeDoesNotBelieveArgument, _.butSheDoesNotBelieveArgument,
                                                 data['gender'])
    else:
        bind = _t.get(_.butTheyDoNotBelieveCounter)
        if data['is_valid']:
            bind = __translation_based_on_gender(_t, _.butHeDoesNotBelieveCounter, _.butSheDoesNotBelieveCounter,
                                                 data['gender'])

    bind = bind.format(start_con, end_tag, start_argument, end_tag)

    confrontation_text = f'{intro} {premise}. {bind}{end_tag} {conclusion}{start_tag}. '
    confrontation_text += f'{gender_think}{end_tag} {confrontation}'

    return confrontation_text, data['gender'] if data['is_valid'] else ''


def __get_confrontation_text_for_rebut(lang, nickname, reply_for_argument, user_arg, user_is_attacking,
                                       sys_conclusion, confrontation, premise, conclusion, my_start_argument,
                                       system_argument):
    """
    Returns the system bubble text for a rebut

    :param lang: ui_locales
    :param nickname: of current user
    :param reply_for_argument: Boolean
    :param user_arg: Argument
    :param user_is_attacking: Boolean
    :param sys_conclusion: String
    :param confrontation: String
    :param premise: String
    :param conclusion: String
    :param my_start_argument: String
    :param system_argument: Counter argument of the system
    :return: String, String
    """
    _t = Translator(lang)

    data = get_name_link_of_arguments_author(system_argument, nickname)
    db_other_nick = data['user'].nickname if data['user'] else ''

    infos = {
        'is_okay': data['is_valid'],
        'lang': lang,
        'nickname': nickname,
        'author': data['link'],
        'gender': data['gender'],
        'user_is_attacking': user_is_attacking,
        'db_other_nick': db_other_nick,
    }

    # has the other user any opinion for the users conclusion?
    has_other_user_opinion = False
    if data['is_valid']:
        if user_arg.argument_uid is None:
            db_vote = DBDiscussionSession.query(ClickedArgument).filter(
                ClickedArgument.argument_uid == user_arg.argument_uid,
                ClickedArgument.author_uid == data['user'].uid,
                ClickedArgument.is_up_vote == True,
                ClickedArgument.is_valid == True).all()
        else:
            db_vote = DBDiscussionSession.query(ClickedStatement).filter(
                ClickedStatement.statement_uid == user_arg.conclusion_uid,
                ClickedStatement.author_uid == data['user'].uid,
                ClickedStatement.is_up_vote == True,
                ClickedStatement.is_valid == True).all()
        has_other_user_opinion = db_vote and len(db_vote) > 0
    infos['has_other_user_opinion'] = has_other_user_opinion

    # distinguish between reply for argument and reply for premise group
    if reply_for_argument:  # reply for argument
        confrontation_text = __get_confrontation_text_for_rebut_as_reply(_t, confrontation, user_arg, conclusion,
                                                                         sys_conclusion, system_argument, infos)

    else:  # reply for premise group
        confrontation_text = __get_confrontation_text_for_rebut_as_pgroup(_t, confrontation, premise, conclusion,
                                                                          my_start_argument, infos)
    return confrontation_text, data['gender']


def __get_confrontation_text_for_rebut_as_reply(_t, confrontation, user_arg, conclusion, sys_conclusion,
                                                system_argument, infos):
    # changing arguments for better understanding
    if not user_arg.is_supportive:
        conclusion = sys_conclusion

    if infos['is_okay']:
        intro = infos['author'] + ' ' + start_tag
        bind = start_content + _t.get(_.otherUsersClaimStrongerArgumentS) + end_tag
        say = __translation_based_on_gender(_t, _.heSays, _.sheSays, infos['gender'])
    else:
        intro = start_content
        bind = start_tag + _t.get(_.otherUsersClaimStrongerArgumentP) + end_tag
        say = _t.get(_.theySay)

    tmp_start_tag = ''
    tmp_end_tag = ''
    if tag_type in confrontation:
        tmp_start_tag = start_argument
        tmp_end_tag = end_tag

    accept = _.accept
    reject = _.reject
    point = ':'
    if infos['lang'] == 'de':
        accept = _.assistance
        reject = _.rejection
        point = ''

    tmp = '{}{}{}'.format(tmp_start_tag, _t.get(accept if system_argument.is_supportive else reject), tmp_end_tag)
    bind = bind.format(tmp)

    confrontation_text = '{}{} {}. {}{}{}{} {}'.format(intro, bind, conclusion, start_tag, say, point, end_tag,
                                                       confrontation)

    return confrontation_text


def __get_confrontation_text_for_rebut_as_pgroup(_t, confrontation, premise, conclusion, start_argument, infos):
    if infos['is_okay']:
        if infos['has_other_user_opinion']:
            intro = infos['author'] + ' ' + start_content + _t.get(_.agreesThat) + ' {}. '
            intro += __translation_based_on_gender(_t, _.strongerStatementM, _.strongerStatementF, infos['gender'])
        elif infos['db_other_nick'] == infos['nickname']:
            intro = infos['author'] + ' ' + start_content
            intro += _t.get(_.earlierYouHadNoOpinitionForThisStatement) + ' ' + _t.get(_.strongerStatementY)
        else:
            intro = infos['author'] + ' ' + start_content
            intro += _t.get(_.otherUserDoesntHaveOpinionForThisStatement) + ' '
            intro += __translation_based_on_gender(_t, _.strongerStatementM, _.strongerStatementF, infos['gender'])

    else:
        intro = start_content + _t.get(_.otherParticipantsDontHaveOpinion) + ' {}. ' + _t.get(_.strongerStatementP)

    tmp = start_argument
    if infos['user_is_attacking']:
        tag = start_pro
        tmp += _t.get(_.accepting)
    else:
        tag = start_con
        tmp += _t.get(_.rejecting)
    tmp += end_tag if len(start_argument) > 0 else ''
    intro = intro.format(premise, tag, tmp, ' ' + end_tag)

    tmp = _t.get(_.strongerStatementEnd)
    if tmp == '':
        tmp += ' '
        conclusion = conclusion[len(start_argument):]

    if infos['db_other_nick'] == infos['nickname']:
        bind = _t.get(_.nowYouSayThat)
    else:
        bind = _t.get(_.theySay)
        if infos['is_okay']:
            bind = __translation_based_on_gender(_t, _.heSays, _.sheSays, infos['gender'])

    confrontation_text = '{} {}. {}{}:{} {}'.format(intro, conclusion, start_tag, bind, end_tag, confrontation)

    return confrontation_text


def __translation_based_on_gender(_t, keyword_m, keyword_f, gender):
    if gender is 'm':
        return _t.get(keyword_m)
    else:
        return _t.get(keyword_f)


def get_name_link_of_arguments_author(argument, nickname, with_link=True):
    """
    Will return author of the argument, if the first supporting user

    :param argument: Argument
    :param nickname: User.nickname
    :param with_link:
    :return:
    """
    user, link, is_valid = get_author_data(argument.author_uid, False, True)
    db_author_of_argument = DBDiscussionSession.query(User).get(argument.author_uid)
    gender = db_author_of_argument.gender if db_author_of_argument else 'n'

    db_anonymous_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()

    # if the data of arguments author is not okay, get the first user, who agrees with the argument
    if argument.author_uid == db_anonymous_user.uid or not is_valid:
        # get nick of current user
        nickname = nickname if nickname is not None else nick_of_anonymous_user
        db_current_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        db_author_of_argument = get_author_or_first_supporter_of_element(argument.uid, db_current_user.uid, True)

        if db_author_of_argument:
            user, link, is_valid = get_author_data(db_author_of_argument.uid, gravatar_on_right_side=False,
                                                   linked_with_users_page=with_link)
            db_author_of_argument = DBDiscussionSession.query(User).get(db_author_of_argument.uid)
            gender = db_author_of_argument.gender if db_author_of_argument else 'n'
        else:
            return {
                'user': None,
                'text': '',
                'gender': 'n',
                'is_valid': False
            }

    return {
        'user': user,
        'link': link if is_valid else '',
        'gender': gender,
        'is_valid': is_valid
    }


def get_author_or_first_supporter_of_element(uid, current_user_uid, is_argument):
    """
    Returns the first user with the same opinion and who is not the anonymous or current user

    :param uid: Argument.uid / Statement.uid
    :param current_user_uid: User.uid
    :param is_argument: Boolean
    :return: MarkedArgument or None
    """

    db_anonymous_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    if is_argument:
        db_mark = DBDiscussionSession.query(MarkedArgument).filter(
            ~MarkedArgument.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            MarkedArgument.argument_uid == uid,
        ).first()
    else:
        db_mark = DBDiscussionSession.query(MarkedStatement).filter(
            ~MarkedStatement.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            MarkedStatement.statement_uid == uid,
        ).first()

    if db_mark:
        return DBDiscussionSession.query(User).get(db_mark.author_uid)

    if is_argument:
        db_click = DBDiscussionSession.query(ClickedArgument).filter(
            ~ClickedArgument.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            ClickedArgument.argument_uid == uid,
        ).first()
    else:
        db_click = DBDiscussionSession.query(ClickedStatement).filter(
            ~ClickedStatement.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            ClickedStatement.statement_uid == uid,
        ).first()

    if db_click:
        return DBDiscussionSession.query(User).get(db_click.author_uid)

    return None
