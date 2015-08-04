import sqlalchemy as sa

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from dbas.database import DBSession, Base

# TODO 3: ORM Relationships

class Issue(Base):
	"""
	issue-table with several column.
	Each issue has text and a creation date
	"""
	__tablename__ = 'issue'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime(timezone=True), default=func.now())

	def __init__(self, text):
		"""
		Initializes a row in current position-table
		"""
		self.text = text

	@classmethod
	def by_text(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Issue).order_by(Issue.text)


class Group(Base):
	"""
	group-table with several column.
	Each group has a name
	"""
	__tablename__ = 'groups'
	uid = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.Text, nullable=False, unique=True)

	#author = orm.relationship("User", backref=__tablename__) # one-to-many

	def __init__(self, name):
		"""
		Initializes a row in current group-table
		"""
		self.name = name

	@classmethod
	def by_name(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Group).order_by(Group.name)

	def group_by_id(group):
		return DBSession.query(Group).filter(Group.name == group).first()


class User(Base):
	"""
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
	"""
	__tablename__ = 'users'
	uid = sa.Column(sa.Integer, primary_key=True)
	firstname = sa.Column(sa.Text, nullable=False)
	surname = sa.Column(sa.Text, nullable=False)
	nickname = sa.Column(sa.Text, nullable=False)
	email = sa.Column(sa.Text, nullable=False, unique=True)
	gender = sa.Column(sa.Text, nullable=False)
	password = sa.Column(sa.Text, nullable=False)
	group_uid = sa.Column(sa.Integer, sa.ForeignKey(Group.uid))
	last_action = sa.Column(sa.DateTime(timezone=True), default=func.now())
	last_login = sa.Column(sa.DateTime(timezone=True), default=func.now())
	registered = sa.Column(sa.DateTime(timezone=True), default=func.now())

	def __init__(self, group, firstname, surname, nickname, email, password, gender):
		"""
		Initializes a row in current user-table
		"""
		self.firstname = firstname
		self.surname = surname
		self.nickname = nickname
		self.email = email
		self.gender = gender
		self.password = password
		self.group_uid = group
		self.last_action = func.now()
		self.last_login = func.now()
		self.registered = func.now()

	@classmethod
	def by_surname(cls):
		"""Return a query of users sorted by surname."""
		return DBSession.query(User).order_by(User.surname)

	def validate_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.check(self.password, password)

	def update_last_logged(self):
		self.last_logged = func.now()

	def update_last_action(self):
		self.last_action = func.now()


class Statement(Base):
	"""
	Statement-table with several columns.
	Each statement has link to its text
	"""
	__tablename__ = 'statements'
	uid = sa.Column(sa.Integer, primary_key=True)
	text_uid = sa.Column(sa.Integer, sa.ForeignKey(TextValue.uid))

	def __init__(self, text):
		"""
		Initializes a row in current statement-table
		"""
		self.text_uid = text


class TextValue(Base):
	"""
	Text-Value-table with several columns.
	Each text value has a link to its most recent text value and a weight
	"""
	__tablename__ = 'textvalue'
	uid = sa.Column(sa.Integer, primary_key=True)
	textVersion_uid = sa.Column(sa.Integer, sa.ForeignKey(TextVersion.uid))

	def __init__(self, textVersion):
		"""
		Initializes a row in current text-value-table
		"""
		self.textVersion_uid = textVersion


class TextVersion(Base):
	"""
	TextVersions-table with several columns.
	Each text versions has link to the recent link and fields for content, author, timestamp and weight
	"""
	__tablename__ = 'textversions'
	uid = sa.Column(sa.Integer, primary_key=True)
	textValue_uid = sa.Column(sa.Integer, sa.ForeignKey(TextValue.uid))
	content = sa.Column(sa.Text, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)

	def __init__(self, text, content, author, weight):
		"""
		Initializes a row in current text versions-table
		"""
		self.textValue_uid = text
		self.content = content
		self.author_uid = author
		self.weight = weight
		self.timestamp = func.now()

	@classmethod
	def by_timestamp(cls):
		"""Return a query of text versions sorted by timestamp."""
		return DBSession.query(TextVersion).order_by(TextVersion.timestamp)

	@classmethod
	def by_weight(cls):
		"""Return a query of text versions sorted by wight."""
		return DBSession.query(TextVersion).order_by(TextVersion.weight)


class PremisseGroup(Base):
	"""
	PremisseGroup-table with several columns.
	Each premissesGroup has a id and an author
	"""
	__tablename__ = 'premissegroups'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))

	def __init__(self, author):
		"""
		Initializes a row in current premissesGroup-table
		"""
		self.author_uid = author


class Premisse(Base):
	"""
	Premisses-table with several columns.
	Each premisses has a value pair of group and statement, an author, a timestamp as well as a boolean whether it is negated
	"""
	__tablename__ = 'premisses'
	premissesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey(PremisseGroup.uid), primary_key=True)
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey(Statement.uid), primary_key=True)
	isNegated = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	ForeignKeyConstraint(['premissesGroup_uid', 'statement_uid'], ['PremisseGroups.uid', 'Statement.uid'])

	def __init__(self, premissesGroup, statement, isNegated, author):
		"""
		Initializes a row in current premisses-table
		"""
		self.premissesGroup_uid = premissesGroup
		self.statement_uid = statement
		self.isNegated = isNegated
		self.author_uid = author
		self.timestamp = func.now()


class Argument(Base):
	"""
	Argument-table with several columns.
	Each argument has justifying statement(s) (premisses) and the the statement-to-be-justified (argument or statement).
	Additionally there is a relation, timestamp, author, weight, ...
	"""
	__tablename__ = 'arguments'
	uid = sa.Column(sa.Integer, primary_key=True)
	premissegroup_uid = sa.Column(sa.Integer, sa.ForeignKey(PremisseGroup.uid))
	conclusion_uid = sa.Column(sa.Integer, sa.ForeignKey(Statement.uid))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey("arguments.uid"))
	isSupportive = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	argument_link = relationship("Argument")#, remote_side=[uid])


	def __init__(self, premissegroup, conclusion, argument, isSupportive, author):
		"""
		Initializes a row in current argument-table
		"""
		self.premissegroup_uid = premissegroup
		self.conclusion_uid = conclusion
		self.argument_uid = argument
		self.isSupportive = isSupportive
		self.author_uid = author


class Track(Base):
	"""
	Track-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'track'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey(Statement.uid))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())

	def __init__(self, user_uid, statement_uid):
		"""
		Initializes a row in current track-table
		"""
		self.user_uid = user_uid
		self.statement_uid = statement_uid
		self.timestamp = func.now()
