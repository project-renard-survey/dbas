import transaction
import datetime
import requests
import urllib
import hashlib
import random

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.session import check_csrf_token
from pyramid.renderers import get_renderer
from pyramid.threadlocal import get_current_registry
from pyshorteners.shorteners import Shortener

from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue, Argument
from .dictionary_helper import DictionaryHelper
from .email import EmailHelper
from .logger import logger
from .query_helper import QueryHelper, UrlManager
from .strings import Translator, TextGenerator
from .string_matcher import FuzzyStringMatcher
from .breadcrumb_helper import BreadcrumbHelper
from .recommender_system import RecommenderHelper, RecommenderHelper
from .user_management import PasswordGenerator, PasswordHandler, UserHandler
from .voting_helper import VotingHelper
from .url_manager import UrlManager

name = 'D-BAS'
version = '0.5.2'
header = name + ' ' + version
issue_fallback = 1
mainpage = ''

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015


class Dbas(object):

	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return: json-dict()
		"""
		self.request = request
		global mainpage
		mainpage = request.application_url
		self.issue_fallback = DBDiscussionSession.query(Issue).first().uid

	def escape_string(self, text):
		"""

		:param text:
		:return: json-dict()
		"""
		return text  # todo escaping string correctly
		# return re.escape(text)

	def base_layout(self):
		renderer = get_renderer('templates/basetemplate.pt')
		layout = renderer.implementation().macros['layout']
		return layout

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
	@forbidden_view_config(renderer='templates/index.pt')
	def main_page(self):
		"""
		View configuration for the main page
		:return: HTTP 200 with several information
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_page', 'def', 'main page')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)
		DictionaryHelper().add_language_options_for_extra_dict(extras_dict, ui_locales)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Main',
			'project': header,
			'extras': extras_dict
		}

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.
		:return: dictionary with title and project username as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_contact', 'def', 'contact page')

		token = self.request.session.new_csrf_token()
		logger('main_contact', 'new token', str(token))

		contact_error = False
		send_message = False
		message = ''

		try:
			ui_locales = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			ui_locales = get_current_registry().settings['pyramid.default_locale_name']

		logger('main_contact', 'form.contact.submitted', 'requesting params')
		username        = self.request.params['name'] if 'name' in self.request.params else ''
		email           = self.request.params['mail'] if 'mail' in self.request.params else ''
		phone           = self.request.params['phone'] if 'phone' in self.request.params else ''
		content         = self.request.params['content'] if 'content' in self.request.params else ''
		spam            = self.request.params['spam'] if 'spam' in self.request.params else ''
		request_token   = self.request.params['csrf_token'] if 'csrf_token' in self.request.params else ''
		logger('main_contact', 'form.contact.submitted', 'name: ' + name + ', mail: ' + email + ', phone: ' + phone + ', content: ' + content + ', spam: ' + spam + ', csrf_token: ' + request_token)

		# get anti-spam-question
		spamquestion, answer = UserHandler().get_random_anti_spam_question(ui_locales)
		# save answer in session
		self.request.session['antispamanswer'] = answer

		if 'form.contact.submitted' in self.request.params:
			_t = Translator(ui_locales)

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# sanity checks
			# check for empty username
			if not username:
				logger('main_contact', 'form.contact.submitted', 'username empty')
				contact_error = True
				message = _t.get(_t.emptyName)

			# check for non valid mail
			elif not is_mail_valid:
				logger('main_contact', 'form.contact.submitted', 'mail is not valid')
				contact_error = True
				message = _t.get(_t.emptyEmail)

			# check for empty content
			elif not content:
				logger('main_contact', 'form.contact.submitted', 'content is empty')
				contact_error = True
				message = _t.get(_t.emtpyContent)

			# check for empty username
			elif (not spam) or (not spam.isdigit()) or (not int(spam) == self.request.session['antispamanswer']):
				logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer' + ', given answer ' + spam + ', right answer ' + str(self.request.session['antispamanswer']))
				contact_error = True
				message = _t.get(_t.maliciousAntiSpam)

			# is the token valid?
			elif request_token != token:
				logger('main_contact', 'form.contact.submitted', 'token is not valid' + ', request_token: ' + str(request_token) + ', token: ' + str(token))
				message = _t.get(_t.nonValidCSRF)
				contact_error = True

			else:
				subject = 'contactDBAS''Contact D-BAS'
				body = _t.get(_t.name) + ': ' + username + '\n'\
				       + _t.get(_t.mail) + ': ' + email + '\n'\
				       + _t.get(_t.phone) + ': ' + phone + '\n'\
				       + _t.get(_t.message) + ':\n' + content
				send_message, message = EmailHelper().send_mail(self.request, subject, body, email, ui_locales)
				contact_error = not send_message

		logger('main_contact', 'form.contact.submitted', 'content: ' + content)
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)
		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Contact',
			'project': header,
			'extras': extras_dict,
			'was_message_send': send_message,
			'contact_error': contact_error,
			'message': message,
			'name': username,
			'mail': email,
			'phone': phone,
			'content': content,
			'spam': '',
			'spamquestion': spamquestion,
			'csrf_token': token
		}

	# content page
	@view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
	def discussion_init(self, for_api=False):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:return: dictionary
		"""
		# '/a*slug'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))

		_qh = QueryHelper()
		_dh = DictionaryHelper()
		slug = self.request.matchdict['slug'][0] if 'slug' in self.request.matchdict and len(self.request.matchdict['slug']) > 0 else ''

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		# update timestamp and manage breadcrumb
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		breadcrumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, self.request.authenticated_userid, slug,
		                                                 self.request.session.id, transaction, ui_locales,
		                                                 mainpage, for_api)

		discussion_dict = _dh.prepare_discussion_dict(issue, ui_locales, at_start=True)
		item_dict       = _dh.prepare_item_dict_for_start(issue, self.request.authenticated_userid, ui_locales, mainpage, for_api)
		extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, False, ui_locales,
		                                          self.request.authenticated_userid, breadcrumbs=breadcrumbs,
		                                          application_url=mainpage, for_api=for_api)

		if len(item_dict) == 0:
			_qh.add_discussion_end_text(discussion_dict, extras_dict, self.request.authenticated_userid, ui_locales, at_start=True)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# attitude page
	@view_config(route_name='discussion_attitude', renderer='templates/content.pt', permission='everybody')
	def discussion_attitude(self, for_api=False):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:return: dictionary
		"""
		# '/d/{slug}/a/{statement_id}'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		_qh = QueryHelper()
		_dh = DictionaryHelper()
		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		statement_id    = matchdict['statement_id'][0] if 'statement_id' in matchdict else ''

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		# update timestamp and manage breadcrumb
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		breadcrumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, self.request.authenticated_userid, slug,
		                                                 self.request.session.id, transaction, ui_locales,
		                                                 mainpage, for_api)

		discussion_dict = _dh.prepare_discussion_dict(statement_id, ui_locales, at_attitude=True)
		if not discussion_dict:
			return HTTPFound(location=UrlManager(for_api=for_api).get_404([slug, statement_id]))

		item_dict       = _dh.prepare_item_dict_for_attitude(statement_id, issue, ui_locales, mainpage, for_api)
		extras_dict     = _dh.prepare_extras_dict(issue_dict['slug'], False, False, True, False, ui_locales,
		                                          self.request.authenticated_userid, breadcrumbs=breadcrumbs,
		                                          application_url=mainpage, for_api=for_api)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# justify page
	@view_config(route_name='discussion_justify', renderer='templates/content.pt', permission='everybody')
	def discussion_justify(self, for_api=False):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:return: dictionary
		"""
		# '/d/{slug}/j/{statement_or_arg_id}/{mode}*relation'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		_qh = QueryHelper()
		_dh = DictionaryHelper()

		slug                = matchdict['slug'] if 'slug' in matchdict else ''
		statement_or_arg_id = matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in matchdict else ''
		mode                = matchdict['mode'] if 'mode' in matchdict else ''
		supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
		relation            = matchdict['relation'][0] if len(matchdict['relation']) > 0 else ''

		issue               = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		ui_locales          = _qh.get_language(self.request, get_current_registry())
		issue_dict          = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		# update timestamp and manage breadcrumb
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		breadcrumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, self.request.authenticated_userid, slug,
		                                                 self.request.session.id, transaction, ui_locales,
		                                                 mainpage, for_api)

		if [c for c in ('t', 'f') if c in mode] and relation == '':
			# justifying position
			logger('discussion_justify', 'def', 'justifying position')
			discussion_dict = _dh.prepare_discussion_dict(statement_or_arg_id, ui_locales, at_justify=True, is_supportive=supportive)
			if not discussion_dict:
				return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_id]))

			item_dict       = _dh.prepare_item_dict_for_justify_statement(statement_or_arg_id, issue, supportive, ui_locales, mainpage, for_api)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, False, ui_locales,
			                                          self.request.authenticated_userid, mode == 't', breadcrumbs=breadcrumbs,
			                                          application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0:
				_qh.add_discussion_end_text(discussion_dict, extras_dict, self.request.authenticated_userid, ui_locales,
				                            at_justify=True, current_premise=_qh.get_text_for_statement_uid(statement_or_arg_id))

		elif 'd' in mode and relation == '':
			# dont know
			logger('discussion_justify', 'def', 'dont know position')
			argument_uid    = RecommenderHelper().get_argument_by_conclusion(statement_or_arg_id, supportive)
			discussion_dict = _dh.prepare_discussion_dict(argument_uid, ui_locales, at_dont_know=True,
			                                              is_supportive=supportive, additional_id=statement_or_arg_id)
			item_dict       = _dh.prepare_item_dict_for_reaction(argument_uid, supportive, issue, ui_locales, mainpage, for_api)
			extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, ui_locales, self.request.authenticated_userid,
			                                          argument_id=argument_uid, breadcrumbs=breadcrumbs, application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0:
				_qh.add_discussion_end_text(discussion_dict, extras_dict, self.request.authenticated_userid, ui_locales, at_dont_know=True)

		elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
			# justifying argument
			logger('discussion_justify', 'def', 'argument stuff')
			is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
			discussion_dict = _dh.prepare_discussion_dict(statement_or_arg_id, ui_locales, at_justify_argumentation=True,
			                                              is_supportive=supportive, attack=relation,
			                                              logged_in=self.request.authenticated_userid)
			item_dict       = _dh.prepare_item_dict_for_justify_argument(statement_or_arg_id, relation, issue, supportive,
			                                                             ui_locales, mainpage, for_api)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, True, ui_locales, self.request.authenticated_userid,
			                                          argument_id=statement_or_arg_id, breadcrumbs=breadcrumbs,
			                                          application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0:
				_qh.add_discussion_end_text(discussion_dict, extras_dict, self.request.authenticated_userid, ui_locales,
				                            at_justify_argumentation=True)
		else:
			return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, 'j', statement_or_arg_id, mode, relation]))

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# reaction page
	@view_config(route_name='discussion_reaction', renderer='templates/content.pt', permission='everybody')
	def discussion_reaction(self, for_api=False):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:return: dictionary
		"""
		# '/d/{slug}/r/{arg_id_user}/{mode}*arg_id_sys'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		arg_id_user     = matchdict['arg_id_user'] if 'arg_id_user' in matchdict else ''
		attack          = matchdict['mode'] if 'mode' in matchdict else ''
		arg_id_sys      = matchdict['arg_id_sys'][0] if len(matchdict['arg_id_sys']) > 0 else ''
		supportive      = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first().is_supportive

		# set votings
		VotingHelper().add_vote_for_argument(arg_id_user, self.request.authenticated_userid, transaction)

		_qh = QueryHelper()
		_dh = DictionaryHelper()

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		# update timestamp and manage breadcrumb
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		breadcrumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, self.request.authenticated_userid, slug,
		                                                 self.request.session.id, transaction, ui_locales,
		                                                 mainpage, for_api)

		discussion_dict = _dh.prepare_discussion_dict(arg_id_user, ui_locales, at_argumentation=True, is_supportive=supportive,
		                                              additional_id=arg_id_sys, attack=attack)
		item_dict       = _dh.prepare_item_dict_for_reaction(arg_id_sys, supportive, issue, ui_locales, mainpage, for_api)
		extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, ui_locales, self.request.authenticated_userid,
		                                          argument_id=arg_id_user, breadcrumbs=breadcrumbs,
		                                          application_url=mainpage, for_api=for_api)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_settings', 'def', 'main')

		token = self.request.session.get_csrf_token()
		logger('main_settings', 'new token', str(token))
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		logger('main_settings', 'language', ui_locales)

		old_pw = ''
		new_pw = ''
		confirm_pw = ''
		message = ''
		error = False
		success = False

		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
		logger('main_settings', 'db_user', db_user.nickname + ' ' + str(db_user.groups.uid) + ' ' + str(db_user.groups.name))
		uh = UserHandler()
		if db_user and 'form.passwordchange.submitted' in self.request.params:
			logger('main_settings', 'form.changepassword.submitted', 'requesting params')
			old_pw = self.request.params['passwordold']
			new_pw = self.request.params['password']
			confirm_pw = self.request.params['passwordconfirm']

			message, error, success = uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, ui_locales)

		# get gravater profile picture
		gravatar_url = uh.get_profile_picture(db_user)

		logger('main_settings', 'return change_error', str(error) + ', change_success' + str(success) + ', message' + str(message))
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)
		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Settings',
			'project': header,
			'extras': extras_dict,
			'passwordold': '' if success else old_pw,
			'password': '' if success else new_pw,
			'passwordconfirm': '' if success else confirm_pw,
			'change_error': error,
			'change_success': success,
			'message': message,
			'db_firstname': db_user.firstname if db_user else 'unknown',
			'db_surname': db_user.surname if db_user else 'unknown',
			'db_nickname': db_user.nickname if db_user else 'unknown',
			'db_mail': db_user.email if db_user else 'unknown',
			'db_group': db_user.groups.name if db_user and db_user.groups else 'unknown',
			'avatar_url': gravatar_url,
			'csrf_token': token
		}

	# admin page, when logged in
	@view_config(route_name='main_admin', renderer='templates/admin.pt', permission='admin')  # or permission='use'
	def main_admin(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_admin', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Admin',
			'project': header,
			'extras': extras_dict
		}

	# news page for everybody
	@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
	def main_news(self):
		"""
		View configuration for the news.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_news', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		is_author = UserHandler().is_user_author(self.request.authenticated_userid)

		# get date
		now = datetime.datetime.now()
		yyyy = str(now.year)
		mm = str(now.month) if now.month > 9 else '0' + str(now.month)
		dd = str(now.day) if now.day > 9 else '0' + str(now.day)
		date = dd + "." + mm + "." + yyyy

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'News',
			'project': header,
			'extras': extras_dict,
			'date': date,
			'is_author': is_author
		}

	# imprint
	@view_config(route_name='main_imprint', renderer='templates/imprint.pt', permission='everybody')
	def main_imprint(self):
		"""
		View configuration for the imprint.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_imprint', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Imprint',
			'project': header,
			'extras': extras_dict
		}

	# 404 page
	@notfound_view_config(renderer='templates/404.pt')
	def notfound(self):
		"""
		View configuration for the 404 page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request')

		logger('notfound', 'def', 'path: ' + self.request.path)
		logger('notfound', 'def', 'view name: ' + self.request.view_name)

		logger('notfound', 'def', 'params:')
		for param in self.request.params:
			logger('notfound', 'def', '    ' + param + ' -> ' + self.request.params[param])

		self.request.response.status = 404
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Error',
			'project': header,
			'page_notfound_viewname': self.request.path,
			'extras': extras_dict
		}

# ####################################
# ADDTIONAL AJAX STUFF # USER THINGS #
# ####################################

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_get_user_history', renderer='json', check_csrf=True)
	def get_user_history(self):
		"""
		Request the complete user track
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_user_history', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		return_dict = BreadcrumbHelper().get_breadcrumbs(self.request.authenticated_userid, ui_locales)
		logger('get_user_history', 'def', str(return_dict))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - deleting complete history of the user
	@view_config(route_name='ajax_delete_user_history', renderer='json', check_csrf=True)
	def delete_user_history(self):
		"""
		Request the complete user history
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_user_history', 'def', 'main')
		BreadcrumbHelper().del_breadcrumbs_of_user(transaction, self.request.authenticated_userid)
		return_dict = dict()
		return_dict['removed_data'] = 'true'  # necessary
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - user login
	@view_config(route_name='ajax_user_login', renderer='json')
	def user_login(self):
		"""
		Will login the user by his nickname and password
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_login', 'def', 'main')

		success = '0'
		message = ''
		return_dict = dict()

		try:
			nickname = self.escape_string(self.request.params['user'])
			password = self.escape_string(self.request.params['password'])
			url = self.request.params['url']
			logger('user_login', 'def', 'params nickname: ' + str(nickname) + ', password: ' + str(password) + ', url: ' + url)

			db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if not db_user:
				logger('user_login', 'no user', 'user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif not db_user.validate_password(password):
				logger('user_login', 'password not valid', 'wrong password')
				message = 'Wrong password'
			else:
				logger('user_login', 'login', 'login successful')
				headers = remember(self.request, nickname)

				# update timestamp
				logger('user_login', 'login', 'update login timestamp')
				db_user.update_last_logged()
				transaction.commit()

				return HTTPFound(
					location=url,
					headers=headers,
				)

		except KeyError as e:
			logger('user_login', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - user login
	@view_config(route_name='ajax_user_logout', renderer='json')
	def user_logout(self):
		"""
		Will logout the user
		:return: HTTPFound with forgotten headers
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_logout', 'def', 'main')

		url = self.request.params['url']

		if 'setting' in url:
			url = mainpage
			logger('user_logout', 'def', 'redirect: ' + url)

		headers = forget(self.request)
		return HTTPFound(
			location=url,
			headers=headers,
		)

	# ajax - registration of users
	@view_config(route_name='ajax_user_registration', renderer='json')
	def user_registration(self):
		"""
		Registers new user
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_registration', 'def', 'main')

		# default values
		success = '0'
		message = ''
		return_dict = dict()

		# getting params
		try:
			params          = self.request.params
			firstname       = self.escape_string(params['firstname'])
			lastname        = self.escape_string(params['lastname'])
			nickname        = self.escape_string(params['nickname'])
			email           = self.escape_string(params['email'])
			gender          = self.escape_string(params['gender'])
			password        = self.escape_string(params['password'])
			passwordconfirm = self.escape_string(params['passwordconfirm'])
			ui_locales      = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())
			logger('user_registration', 'def', 'params firstname: ' + str(firstname)
			       + ', lastname: ' + str(lastname)
			       + ', nickname: ' + str(nickname)
			       + ', email: ' + str(email)
			       + ', password: ' + str(password)
			       + ', passwordconfirm: ' + str(passwordconfirm)
			       + ', lang: ' + ui_locales)

			_t = Translator(ui_locales)

			# database queries mail verification
			db_nick = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
			logger('user_registration', 'main', 'Validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('user_registration', 'main', 'Passwords are not equal')
				message = _t.get(_t.pwdNotEqual)
			# is the nick already taken?
			elif db_nick:
				logger('user_registration', 'main', 'Nickname \'' + nickname + '\' is taken')
				message = _t.get(_t.nickIsTaken)
			# is the email already taken?
			elif db_mail:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is taken')
				message = _t.get(_t.mailIsTaken)
			# is the email valid?
			elif not is_mail_valid:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is not valid')
				message = _t.get(_t.mailNotValid)
			# is the token valid?
			# elif request_token != token :
			# 	logger('user_registration', 'main', 'token is not valid')
			# 	logger('user_registration', 'main', 'request_token: ' + str(request_token))
			# 	logger('user_registration', 'main', 'token: ' + str(token))
			# 	message = 'CSRF-Token is not valid'
			else:
				# getting the editors group
				db_group = DBDiscussionSession.query(Group).filter_by(name="editors").first()

				# does the group exists?
				if not db_group:
					message = _t.get(_t.errorTryLateOrContant)
					logger('user_registration', 'main', 'Error occured')
				else:
					# creating a new user with hased password
					logger('user_registration', 'main', 'Adding user')
					hashed_password = PasswordHandler().get_hashed_password(password)
					newuser = User(firstname=firstname,
					               surname=lastname,
					               email=email,
					               nickname=nickname,
					               password=hashed_password,
					               gender=gender,
					               group=db_group.uid)
					DBDiscussionSession.add(newuser)
					transaction.commit()

					# sanity check, whether the user exists
					checknewuser = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
					if checknewuser:
						logger('user_registration', 'main', 'New data was added with uid ' + str(checknewuser.uid))
						message = _t.get(_t.accountWasAdded)
						success = '1'

						# sending an email
						subject = 'D-BAS Account Registration'
						body = _t.get(_t.accountWasRegistered)
						EmailHelper().send_mail(self.request, subject, body, email, ui_locales)

					else:
						logger('user_registration', 'main', 'New data was not added')
						message = _t.get(_t.accoutErrorTryLateOrContant)

		except KeyError as e:
			logger('user_registration', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - password requests
	@view_config(route_name='ajax_user_password_request', renderer='json')
	def user_password_request(self):
		"""
		Sends an email, when the user requests his password
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_password_request', 'def', 'main')

		success = '0'
		message = ''
		return_dict = dict()

		try:
			email = self.escape_string(self.request.params['email'])
			ui_locales      = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())
			logger('user_password_request', 'def', 'params email: ' + str(email) + ', ui_locales ' + ui_locales)
			success = '1'
			_t = Translator(ui_locales)

			db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = PasswordGenerator().get_rnd_passwd()
				logger('user_password_request', 'form.passwordrequest.submitted', 'New password is ' + pwd)
				hashedpwd = PasswordHandler().get_hashed_password(pwd)
				logger('user_password_request', 'form.passwordrequest.submitted', 'New hashed password is ' + hashedpwd)

				# set the hased one
				db_user.password = hashedpwd
				DBDiscussionSession.add(db_user)
				transaction.commit()

				body = _t.get(_t.nicknameIs) + db_user.nickname + '\n'
				body += _t.get(_t.newPwdIs) + pwd
				subject = _t.get(_t.dbasPwdRequest)
				reg_success, message = EmailHelper().send_mail(self.request, subject, body, email, ui_locales)

				# logger
				if reg_success:
					logger('user_password_request', 'form.passwordrequest.submitted', 'New password was sent')
					success = '1'
				else:
					logger('user_password_request', 'form.passwordrequest.submitted', 'Error occured')
			else:
				logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'emailUnknown'

		except KeyError as e:
			logger('user_password_request', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

	# ajax - send new start statement
	@view_config(route_name='ajax_set_new_start_statement', renderer='json', check_csrf=True)
	def set_new_start_statement(self, for_api=False):
		"""
		Inserts a new statement into the database, which should be available at the beginning
		:param for_api: boolean
		:return: a status code, if everything was successfull
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_start_statement', 'def', 'ajax, self.request.params: ' + str(self.request.params))
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_new_start_statement', 'def', 'main')

		return_dict = dict()
		return_dict['error'] = ''
		try:
			statement   = self.request.params['statement']
			issue       = QueryHelper().get_issue(self.request)
			slug        = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
			logger('set_new_start_statement', 'def', 'request data: statement ' + str(statement))
			new_statement, is_duplicate = QueryHelper().set_statement(transaction, statement, self.request.authenticated_userid, True, issue)
			if new_statement == -1:
				return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty)
			else:
				url = UrlManager(mainpage, slug, for_api).get_url_for_statement_attitude(False, new_statement.uid)
				return_dict['url'] = url
				logger('set_new_start_statement', 'def', 'return url ' + url)
		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new start premise
	@view_config(route_name='ajax_set_new_start_premise', renderer='json', check_csrf=True)
	def set_new_start_premise(self, for_api=False):
		"""
		Sets new premise for the start
		:param for_api: boolean
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_start_premise', 'def', 'ajax, self.request.params: ' + str(self.request.params))
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)

		logger('set_new_start_premise', 'def', 'main')

		return_dict = dict()
		_qh = QueryHelper()
		_dh = DictionaryHelper()
		_tn = Translator(_qh.get_language(self.request, get_current_registry()))

		try:
			logger('set_new_start_premise', 'def', 'getting params')
			premisegroups   = _dh.string_to_json(self.request.params['premisegroups'])
			conclusion_id   = self.request.params['conclusion_id']
			supportive      = True if self.request.params['supportive'].lower() == 'true' else False
			issue           = _qh.get_issue(self.request)
			logger('set_new_start_premise', 'def', 'conclusion_id: ' + str(conclusion_id) + ', premisegroups: ' + str(premisegroups) +
			       ', supportive: ' + str(supportive) + ', issue: ' + str(issue))

			new_arguments = []
			for group in premisegroups:
				logger('set_new_start_premise', 'def', 'found text: ' + str(group))
				new_argument_uid = _qh.set_premises_as_group_for_conclusion(transaction, user_id, group, conclusion_id, supportive, issue)
				if new_argument_uid == -1:
					return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty)
					logger('set_new_start_premise', 'def', 'return because input is empty')
					return _dh.dictionary_to_json_array(return_dict, True)
					
				new_arguments.append(new_argument_uid)
				logger('set_new_start_premise', 'def', 'new argument created: ' + str(new_argument_uid))

			new_argument_uid    = random.choice(new_arguments)  # TODO IMPROVE / eliminate random
			arg_id_sys, attack  = RecommenderHelper().get_attack_for_argument(new_argument_uid, issue)
			slug                = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()

			url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
			return_dict['url']      = url
			return_dict['error']    = ''
		except KeyError as e:
			logger('set_new_start_premise', 'error', repr(e))
			return_dict['error']    = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_json = _dh.dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new premises
	@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json', check_csrf=True)
	def set_new_premises_for_argument(self, for_api=False):
		"""
		Sets a new premisse for an argument
		:param for_api: boolean
		:return: json-dict()
		"""
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_premises_for_argument', 'def', 'ajax, self.request.params: ' + str(self.request.params))

		logger('set_new_premises_for_argument', 'def', 'main')

		return_dict = dict()
		_dh = DictionaryHelper()
		_tn = Translator(_qh.get_language(self.request, get_current_registry()))

		try:
			logger('set_new_premises_for_argument', 'def', 'getting params')
			arg_uid         = self.request.params['arg_uid']
			attack_type     = self.request.params['attack_type']
			premisegroups   = _dh.string_to_json(self.request.params['premisegroups'])
			supportive      = self.request.params['supportive']

			issue = QueryHelper().get_issue(self.request)
			logger('set_new_premises_for_argument', 'def', 'arg_uid: ' + str(arg_uid) + ', premisegroups: ' + str(premisegroups) +
			       ', relation: ' + str(attack_type) + ', supportive ' + str(supportive) + ', issue: ' + str(issue))

			new_arguments = []
			for group in premisegroups:
				logger('set_new_premises_for_argument', 'def', 'found text: ' + str(group))

				new_argument_uid = QueryHelper().handle_insert_new_premises_for_argument(group, attack_type, arg_uid, issue,
				                                                                         self.request.authenticated_userid,
				                                                                         transaction)
				if new_argument_uid == -1:
					return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseEmpty)
					logger('set_new_start_premise', 'def', 'return because input is empty')
					return _dh.dictionary_to_json_array(return_dict, True)

				new_arguments.append(new_argument_uid)

			if len(new_arguments) == 0:
				return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseEmpty)
			else:
				new_argument_uid = random.choice(new_arguments)  # TODO IMPROVE / eliminate random
				logger('set_new_premises_for_argument', 'def', 'new_argument_uid ' + str(new_argument_uid))

				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(new_argument_uid, issue)
				if arg_id_sys == 0:
					attack = 'end'

				slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
				url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
				return_dict['url']      = url
				return_dict['error']    = ''
		except KeyError as e:
			logger('set_new_premises_for_argument', 'error', repr(e))
			return_dict['status'] = '-1'
			return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_json = _dh.dictionary_to_json_array(return_dict, True)

		logger('set_new_premises_for_argument', 'def', 'returning')
		return return_json

	# ajax - set new textvalue for a statement
	@view_config(route_name='ajax_set_correcture_of_statement', renderer='json', check_csrf=True)
	def set_correcture_of_statement(self):
		"""
		Sets a new textvalue for a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_correcture_of_statement', 'def', 'main')

		try:
			uid = self.request.params['uid']
			corrected_text = self.escape_string(self.request.params['text'])
			logger('set_correcture_of_statement', 'def', 'params uid: ' + str(uid) + ', corrected_text: ' + str(corrected_text))
			return_dict = QueryHelper().correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text)
		except KeyError as e:
			return_dict = dict()
			logger('set_correcture_of_statement', 'error', repr(e))

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################

	# ajax - getting changelog of a statement
	@view_config(route_name='ajax_get_logfile_for_statement', renderer='json', check_csrf=False)
	def get_logfile_for_statement(self):
		"""
		Returns the changelog of a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_logfile_for_statement', 'def', 'main')

		return_dict = dict()
		try:
			uid = self.request.params['uid']

			logger('get_logfile_for_statement', 'def', 'params uid: ' + str(uid))
			return_dict = QueryHelper().get_logfile_for_statement(uid)
			return_dict['status'] = 1
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))
			return_dict['status'] = 0

		# return_dict = QueryHelper().get_logfile_for_premisegroup(uid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for shorten url
	@view_config(route_name='ajax_get_shortened_url', renderer='json')
	def get_shortened_url(self):
		"""
		Shortens url with the help of a python lib
		:return: dictionary with shortend url
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_shortened_url', 'def', 'main')

		return_dict = dict()
		# google_api_key = 'AIzaSyAw0aPsBsAbqEJUP_zJ9Fifbhzs8xkNSw0' # browser is
		# google_api_key = 'AIzaSyDneaEJN9FNGUpXHDZahe9Rhb21FsFNS14' # server id
		# bitly_login = 'dbashhu'
		# bitly_token = ''
		# bitly_key = 'R_d8c4acf2fb554494b65529314d1e11d1'

		try:
			url = self.request.params['url']
			# service = 'GoogleShortener'
			# service = 'BitlyShortener'
			service = 'TinyurlShortener'
			# service_url = 'https://goo.gl/'
			# service_url = 'https://bitly.com/'
			service_url = 'http://tinyurl.com/'
			logger('get_shortened_url', 'def', service + ' will shorten ' + str(url))

			# shortener = Shortener(service, api_key=google_api_key)
			# shortener = Shortener(service, bitly_login=bitly_login, bitly_api_key=bitly_key, bitly_token=bitly_token)
			shortener = Shortener(service)

			short_url = format(shortener.short(url))
			return_dict['url'] = short_url
			return_dict['service'] = service
			return_dict['service_url'] = service_url
			logger('get_shortened_url', 'def', 'short url ' + short_url)

			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_shortened_url', 'error', repr(e))
			return_dict['status'] = '0'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)
		return return_json

	# ajax - for attack overview
	@view_config(route_name='ajax_get_argument_overview', renderer='json')
	def get_argument_overview(self):
		"""
		Returns all attacks, done by the users
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		logger('get_argument_overview', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		issue = QueryHelper().get_issue(self.request)
		return_dict = QueryHelper().get_attack_overview(self.request.authenticated_userid, issue, ui_locales)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting all news
	@view_config(route_name='ajax_get_news', renderer='json')
	def get_news(self):
		"""
		ajax interface for getting news
		:return: json-set with all news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_news', 'def', 'main')
		return_dict = QueryHelper().get_news()
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting database
	@view_config(route_name='ajax_get_database_dump', renderer='json')
	def get_database_dump(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_database_dump', 'def', 'main')
		issue = QueryHelper().get_issue(self.request)
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		return_dict = QueryHelper().get_dump(issue, ui_locales)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting all users
	@view_config(route_name='ajax_all_users', renderer='json')
	def get_all_users(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_all_users', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		return_dict = QueryHelper().get_all_users(self.request.authenticated_userid, ui_locales)
		logger('get_all_users', 'def', 'user count ' + str(len(return_dict)))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json


# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################

	# ajax - for language switch
	@view_config(route_name='ajax_switch_language', renderer='json')
	def switch_language(self):
		"""
		Switches the language
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('switch_language', 'def', 'main')

		return_dict = dict()
		try:
			ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())
			logger('switch_language', 'def', 'params uid: ' + str(ui_locales))
			self.request.response.set_cookie('_LOCALE_', str(ui_locales))
			return_dict['status'] = '1'
		except KeyError as e:
			logger('swich_language', 'error', repr(e))
			return_dict['status'] = '0'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)
		return return_json

	# ajax - for sending news
	@view_config(route_name='ajax_send_news', renderer='json')
	def send_news(self):
		"""
		ajax interface for settings news
		:return: json-set with new news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		try:
			title = self.escape_string(self.request.params['title'])
			text = self.escape_string(self.request.params['text'])
			return_dict = QueryHelper().set_news(transaction, title, text, self.request.authenticated_userid)
		except KeyError as e:
			return_dict = dict()
			logger('send_news', 'error', repr(e))
			return_dict['status'] = '-1'

		logger('send_news', 'def', 'main')
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for fuzzy search
	@view_config(route_name='ajax_fuzzy_search', renderer='json')
	def fuzzy_search(self):
		"""
		ajax interface for fuzzy string search
		:return: json-set with all matched strings
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('fuzzy_search', 'main', 'def')
		try:
			value = self.request.params['value']
			mode = str(self.request.params['type'])
			issue = QueryHelper().get_issue(self.request)

			logger('fuzzy_search', 'main', 'value: ' + str(value) + ', mode: ' + str(mode) + ', issue: ' + str(issue))
			return_dict = dict()
			# return_dict['distance_name'] = 'SequenceMatcher'  # TODO improve fuzzy search
			return_dict['distance_name'] = 'Levensthein'
			if mode == '0':  # start statement
				return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, True)
			elif mode == '1':  # edit statement popup
				statement_uid = self.request.params['extra']
				return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_edits(value, statement_uid, issue)
			elif mode == '2':  # start premise
				return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, False)
			elif mode == '3':  # adding reasons
				return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_reasons(value, issue)
			else:
				logger('fuzzy_search', 'main', 'unkown mode: ' + str(mode))
		except KeyError as e:
			return_dict = dict()
			logger('fuzzy_search', 'error', repr(e))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for additional service
	@view_config(route_name='ajax_additional_service', renderer='json')
	def additional_service(self):
		"""

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('additional_service', 'main', 'def')
		rtype = self.request.params['type']

		if rtype == "chuck":
			data = requests.get('http://api.icndb.com/jokes/random')
		else:
			data = requests.get('http://api.yomomma.info/')

		for a in data.json():
			logger('additional_service', 'main', str(a) + ': ' + str(data.json()[a]))

		return data.json()
