import unittest

import os

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession

dir_name = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
settings = appconfig('config:' + os.path.join(dir_name, 'development.ini'))


class InputValidatorTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.input_validator import Validator
        return Validator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_check_for_integer(self):
        reaction = self._makeOne()

        # conditions_response
        ignore_empty_case_len_zero_true = reaction.check_for_integer(input='',
                                                                     ignoreEmptyCase=True)
        self.assertEqual(ignore_empty_case_len_zero_true, True)

        ignore_empty_case_len_false = reaction.check_for_integer(input='str',
                                                                 ignoreEmptyCase=True)
        self.assertEqual(ignore_empty_case_len_false, False)

        not_ignore_empty_case_len_zero_false = reaction.check_for_integer(input='',
                                                                          ignoreEmptyCase=False)
        self.assertEqual(not_ignore_empty_case_len_zero_false, False)

        not_ignore_empty_case_len_false = reaction.check_for_integer(input='str',
                                                                     ignoreEmptyCase=False)
        self.assertEqual(not_ignore_empty_case_len_false, False)

        ignore_empty_case_int_true = reaction.check_for_integer(input=123,
                                                                ignoreEmptyCase=True)
        self.assertEqual(ignore_empty_case_int_true, True)

        not_ignore_empty_case_int_true = reaction.check_for_integer(input=1,
                                                                    ignoreEmptyCase=False)
        self.assertEqual(not_ignore_empty_case_int_true, True)


    def test_check_reaction(self):
        reaction = self._makeOne()

        DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

        # undermine
        undermine_true = reaction.check_reaction(attacked_arg_uid=2,
                                                 attacking_arg_uid=19,
                                                 relation='undermine',
                                                 is_history=False)
        self.assertEqual(undermine_true, True)

        # relation_conditions_ishistory
        undermine_not_db_attacking_arg_false = reaction.check_reaction(attacked_arg_uid=2,
                                                                       attacking_arg_uid=1,
                                                                       relation='undermine',
                                                                       is_history=False)
        self.assertEqual(undermine_not_db_attacking_arg_false, False)

        undermine_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=19,
                                                                  relation='undermine',
                                                                  is_history=False)
        self.assertEqual(undermine_db_attacked_arg_false, False)

        undermine_false = reaction.check_reaction(attacked_arg_uid=0,
                                                  attacking_arg_uid=0,
                                                  relation='undermine',
                                                  is_history=False)
        self.assertEqual(undermine_false, False)

        undermine_empty_string_false = reaction.check_reaction(attacked_arg_uid='',
                                                               attacking_arg_uid='',
                                                               relation='undermine',
                                                               is_history=False)
        self.assertEqual(undermine_empty_string_false, False)

        undermine_string_false = reaction.check_reaction(attacked_arg_uid='2str/',
                                                         attacking_arg_uid='19str',
                                                         relation='undermine',
                                                         is_history=True)
        self.assertEqual(undermine_string_false, False)

        # undercut
        undercut_true = reaction.check_reaction(attacked_arg_uid=1,
                                                attacking_arg_uid=17,
                                                relation='undercut',
                                                is_history=False)
        self.assertEqual(undercut_true, True)

        undercut_false = reaction.check_reaction(attacked_arg_uid=0,
                                                 attacking_arg_uid=0,
                                                 relation='undercut',
                                                 is_history=False)
        self.assertEqual(undercut_false, False)

        undercut_empty_string_false = reaction.check_reaction(attacked_arg_uid='',
                                                              attacking_arg_uid='',
                                                              relation='undercut',
                                                              is_history=False)
        self.assertEqual(undercut_empty_string_false, False)

        undercut_string_false = reaction.check_reaction(attacked_arg_uid='1str/',
                                                        attacking_arg_uid='17str',
                                                        relation='undercut',
                                                        is_history=True)
        self.assertEqual(undercut_string_false, False)

        # rebut
        rebut_true = reaction.check_reaction(attacked_arg_uid=31,
                                             attacking_arg_uid=35,
                                             relation='rebut',
                                             is_history=False)
        self.assertEqual(rebut_true, True)

        rebut_not_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=35,
                                                                  relation='rebut',
                                                                  is_history=False)
        self.assertEqual(rebut_not_db_attacked_arg_false, False)

        rebut_not_db_attacking_arg_false = reaction.check_reaction(attacked_arg_uid=31,
                                                                   attacking_arg_uid=1,
                                                                   relation='rebut',
                                                                   is_history=False)
        self.assertEqual(rebut_not_db_attacking_arg_false, False)

        rebut_not_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=35,
                                                                  relation='rebut',
                                                                  is_history=False)
        self.assertEqual(rebut_not_db_attacked_arg_false, False)

        # db_attacked_arg and db_attacking_arg are False
        rebut_false = reaction.check_reaction(attacked_arg_uid=0,
                                              attacking_arg_uid=0,
                                              relation='rebut',
                                              is_history=False)
        self.assertEqual(rebut_false, False)

        rebut_empty_string_false = reaction.check_reaction(attacked_arg_uid='',
                                                           attacking_arg_uid='',
                                                           relation='rebut',
                                                           is_history=False)
        self.assertEqual(rebut_empty_string_false, False)

        rebut_string_false = reaction.check_reaction(attacked_arg_uid='31str/',
                                                     attacking_arg_uid='35str',
                                                     relation='rebut',
                                                     is_history=True)
        self.assertEqual(rebut_string_false, False)

        # end
        end_attacking_arg_uid_not_zero_true = reaction.check_reaction(attacked_arg_uid=1,
                                                                      attacking_arg_uid=0,
                                                                      relation='end',
                                                                      is_history=False)
        self.assertEqual(end_attacking_arg_uid_not_zero_true, True)

        end_attacking_arg_uid_not_zero_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                       attacking_arg_uid=1,
                                                                       relation='end',
                                                                       is_history=False)
        self.assertEqual(end_attacking_arg_uid_not_zero_false, False)

        end_not_is_history_false = reaction.check_reaction(attacked_arg_uid=1,
                                                           attacking_arg_uid=0,
                                                           relation='end',
                                                           is_history=True)
        self.assertEqual(end_not_is_history_false, False)

        end_empty_string_false = reaction.check_reaction(attacked_arg_uid='',
                                                         attacking_arg_uid='',
                                                         relation='end',
                                                         is_history=False)
        self.assertEqual(end_empty_string_false, False)

        end_string_false = reaction.check_reaction(attacked_arg_uid='1str/',
                                                   attacking_arg_uid='str',
                                                   relation='end',
                                                   is_history=False)
        self.assertEqual(end_string_false, False)
