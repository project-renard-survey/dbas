import unittest

import dbas.review.helper.history as ReviewHistoryHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewHistoryHelper(unittest.TestCase):

    def test_flag_argument(self):
        history = ReviewHistoryHelper.get_complete_review_history('mainpage', 'nickname', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])

        history = ReviewHistoryHelper.get_complete_review_history('mainpage', 'Tobias', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertTrue(history['has_access'])

        history = ReviewHistoryHelper.get_complete_review_history('mainpage', 'Pascal', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])

    def test_get_reputation_history_of(self):
        self.assertEqual(len(ReviewHistoryHelper.get_reputation_history_of('Bla', Translator('en'))), 0)
        history = ReviewHistoryHelper.get_reputation_history_of('Tobias', Translator('en'))
        self.assertTrue(len(history) > 0)
        self.assertTrue('count' in history)
        self.assertTrue('history' in history)
        for h in history['history']:
            self.assertTrue('date' in h)
            self.assertTrue('action' in h)
            self.assertTrue('points' in h)