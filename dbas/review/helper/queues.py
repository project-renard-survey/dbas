"""
Provides helping function for displaying the review queues and locking entries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, ReviewOptimization, TextVersion, \
    LastReviewerOptimization, ReviewEdit, LastReviewerEdit, OptimizationReviewLocks, ReviewEditValue, get_now, \
    Statement, ReviewDuplicate, LastReviewerDuplicate, Argument, Premise, ReviewMerge, ReviewSplit, \
    LastReviewerMerge, LastReviewerSplit
from dbas.lib import get_profile_picture, is_user_author_or_admin
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of, reputation_icons
from dbas.review.helper.subpage import reputation_borders
from dbas.strings.keywords import Keywords as _
from sqlalchemy import and_

max_lock_time_in_sec = 180

key_deletes = 'deletes'
key_optimizations = 'optimizations'
key_edits = 'edits'
key_duplicates = 'duplicates'
key_merge = 'merges'
key_split = 'splits'
key_history = 'history'
key_ongoing = 'ongoing'


def get_review_queues_as_lists(main_page, translator, nickname):
    """
    Prepares dictionary for the edit section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Array
    """
    logger('ReviewQueues', 'get_review_queues_as_lists', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None
    count, all_rights = get_reputation_of(nickname)

    review_list = list()
    review_list.append(__get_delete_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_optimization_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_edit_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_duplicates_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_split_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_merge_dict(main_page, translator, nickname, count, all_rights))
    review_list.append(__get_history_dict(main_page, translator, count, all_rights))
    if is_user_author_or_admin(nickname):
        review_list.append(__get_ongoing_dict(main_page, translator))

    return review_list


def get_complete_review_count(nickname):
    """
    Sums up the review points of the user

    :param nickname: User.nickname
    :return: int
    """
    count, all_rights = get_reputation_of(nickname)

    rights1 = count >= reputation_borders[key_deletes] or all_rights
    rights2 = count >= reputation_borders[key_optimizations] or all_rights
    rights3 = count >= reputation_borders[key_edits] or all_rights
    rights4 = count >= reputation_borders[key_duplicates] or all_rights
    rights5 = count >= reputation_borders[key_split] or all_rights
    rights6 = count >= reputation_borders[key_merge] or all_rights

    count = [
        __get_review_count_for(ReviewDelete, LastReviewerDelete, nickname) if rights1 else 0,
        __get_review_count_for(ReviewOptimization, LastReviewerOptimization, nickname) if rights2 else 0,
        __get_review_count_for(ReviewEdit, LastReviewerEdit, nickname) if rights3 else 0,
        __get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, nickname) if rights4 else 0,
        __get_review_count_for(ReviewSplit, LastReviewerSplit, nickname) if rights5 else 0,
        __get_review_count_for(ReviewMerge, LastReviewerMerge, nickname) if rights6 else 0,
    ]

    return sum(count)


def __get_delete_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = __get_review_count_for(ReviewDelete, LastReviewerDelete, nickname)

    tmp_dict = {'task_name': translator.get(_.queueDelete),
                'id': 'deletes',
                'url': main_page + '/review/' + key_deletes,
                'icon': reputation_icons[key_deletes],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_deletes] or all_rights,
                'is_allowed_text': translator.get(_.visitDeleteQueue),
                'is_not_allowed_text': translator.get(_.visitDeleteQueueLimitation).format(str(reputation_borders[key_deletes])),
                'last_reviews': __get_last_reviewer_of(LastReviewerDelete, main_page)
                }
    return tmp_dict


def __get_optimization_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_optimization_dict', 'main')
    task_count = __get_review_count_for(ReviewOptimization, LastReviewerOptimization, nickname)

    tmp_dict = {'task_name': translator.get(_.queueOptimization),
                'id': 'optimizations',
                'url': main_page + '/review/' + key_optimizations,
                'icon': reputation_icons[key_optimizations],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_optimizations] or all_rights,
                'is_allowed_text': translator.get(_.visitOptimizationQueue),
                'is_not_allowed_text': translator.get(_.visitOptimizationQueueLimitation).format(str(reputation_borders[key_optimizations])),
                'last_reviews': __get_last_reviewer_of(LastReviewerOptimization, main_page)
                }
    return tmp_dict


def __get_edit_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_edit_dict', 'main')
    task_count = __get_review_count_for(ReviewEdit, LastReviewerEdit, nickname)

    tmp_dict = {'task_name': translator.get(_.queueEdit),
                'id': 'edits',
                'url': main_page + '/review/' + key_edits,
                'icon': reputation_icons[key_edits],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_edits] or all_rights,
                'is_allowed_text': translator.get(_.visitEditQueue),
                'is_not_allowed_text': translator.get(_.visitEditQueueLimitation).format(str(reputation_borders[key_edits])),
                'last_reviews': __get_last_reviewer_of(LastReviewerEdit, main_page)
                }
    return tmp_dict


def __get_duplicates_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_duplicates_dict', 'main')
    task_count = __get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, nickname)

    tmp_dict = {'task_name': translator.get(_.queueDuplicates),
                'id': 'duplicates',
                'url': main_page + '/review/' + key_duplicates,
                'icon': reputation_icons[key_duplicates],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_duplicates] or all_rights,
                'is_allowed_text': translator.get(_.visitDuplicateQueue),
                'is_not_allowed_text': translator.get(_.visitDuplicateQueueLimitation).format(str(reputation_borders[key_duplicates])),
                'last_reviews': __get_last_reviewer_of(LastReviewerDuplicate, main_page)
                }
    return tmp_dict


def __get_split_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = __get_review_count_for(ReviewSplit, LastReviewerSplit, nickname)

    tmp_dict = {'task_name': translator.get(_.queueSplit),
                'id': 'splits',
                'url': main_page + '/review/' + key_split,
                'icon': reputation_icons[key_split],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_split] or all_rights,
                'is_allowed_text': translator.get(_.visitSplitQueue),
                'is_not_allowed_text': translator.get(_.visitSplitQueueLimitation).format(str(reputation_borders[key_split])),
                'last_reviews': __get_last_reviewer_of(LastReviewerSplit, main_page)
                }
    return tmp_dict


def __get_merge_dict(main_page, translator, nickname, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = __get_review_count_for(ReviewMerge, LastReviewerMerge, nickname)

    tmp_dict = {'task_name': translator.get(_.queueMerge),
                'id': 'merges',
                'url': main_page + '/review/' + key_merge,
                'icon': reputation_icons[key_merge],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_merge] or all_rights,
                'is_allowed_text': translator.get(_.visitMergeQueue),
                'is_not_allowed_text': translator.get(_.visitMergeQueueLimitation).format(str(reputation_borders[key_merge])),
                'last_reviews': __get_last_reviewer_of(LastReviewerMerge, main_page)
                }
    return tmp_dict


def __get_history_dict(main_page, translator, count, all_rights):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_history_dict', 'main')
    tmp_dict = {'task_name': translator.get(_.queueHistory),
                'id': 'flags',
                'url': main_page + '/review/' + key_history,
                'icon': reputation_icons[key_history],
                'task_count': __get_review_count_for_history(True),
                'is_allowed': count >= reputation_borders[key_history] or all_rights,
                'is_allowed_text': translator.get(_.visitHistoryQueue),
                'is_not_allowed_text': translator.get(_.visitHistoryQueueLimitation).format(str(reputation_borders[key_history])),
                'last_reviews': list()
                }
    return tmp_dict


def __get_ongoing_dict(main_page, translator):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_ongoing_dict', 'main')
    key = 'ongoing'
    tmp_dict = {'task_name': translator.get(_.queueOngoing),
                'id': 'flags',
                'url': main_page + '/review/' + key,
                'icon': reputation_icons[key_ongoing],
                'task_count': __get_review_count_for_history(False),
                'is_allowed': True,
                'is_allowed_text': translator.get(_.visitOngoingQueue),
                'is_not_allowed_text': '',
                'last_reviews': list()
                }
    return tmp_dict


def __get_review_count_for(review_type, last_reviewer_type, nickname):
    """
    Returns the count of reviews of *review_type* for the user with *nickname*, whereby all reviewed data
    of *last_reviewer_type* is not observed

    :param review_type: ReviewEdit, ReviewOptimization or ...
    :param last_reviewer_type: LastReviewerEdit, LastReviewer...
    :param nickname: Users nickname
    :return: Integer
    """
    #  logger('ReviewQueues', '__get_review_count_for', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        db_reviews = DBDiscussionSession.query(review_type).filter_by(is_executed=False).all()
        return len(db_reviews)

    # get all reviews but filter reviews, which
    # - the user has detected
    # - the user has reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = []
    for last_review in db_last_reviews_of_user:
        already_reviewed.append(last_review.review_uid)
    db_reviews = DBDiscussionSession.query(review_type).filter(and_(review_type.is_executed == False,
                                                                    review_type.detector_uid != db_user.uid))

    if len(already_reviewed) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))
    db_reviews = db_reviews.all()

    return len(db_reviews)


def __get_review_count_for_history(is_executed):
    """

    :param is_executed:
    :return:
    """
    db_optimizations = DBDiscussionSession.query(ReviewOptimization).filter_by(is_executed=is_executed).all()
    db_deletes = DBDiscussionSession.query(ReviewDelete).filter_by(is_executed=is_executed).all()
    db_edits = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=is_executed).all()
    return len(db_optimizations) + len(db_deletes) + len(db_edits)


def __get_last_reviewer_of(reviewer_type, main_page):
    """
    Returns a list with the last reviewers of the given type. Multiple reviewers are filtered

    :param reviewer_type:
    :param main_page:
    :return:
    """
    #  logger('ReviewQueues', '__get_last_reviewer_of', 'main')
    users_array = list()
    db_reviews = DBDiscussionSession.query(reviewer_type).order_by(reviewer_type.uid.desc()).all()
    limit = min(5, len(db_reviews))
    index = 0
    while index < limit:
        db_review = db_reviews[index]
        db_user = DBDiscussionSession.query(User).get(db_review.reviewer_uid)
        if db_user:
            tmp_dict = dict()
            tmp_dict['img_src'] = get_profile_picture(db_user, 40)
            tmp_dict['url'] = main_page + '/user/' + str(db_user.uid)
            tmp_dict['name'] = db_user.get_global_nickname()
            # skip it, if it is already in
            if tmp_dict in users_array:
                limit += 1 if len(db_reviews) > limit else 0
            else:
                users_array.append(tmp_dict)
        else:
            limit += 1 if len(db_reviews) > limit else 0
        index += 1
    return users_array


def add_proposals_for_statement_corrections(elements, nickname, translator):
    """
    Add a proposal to correct a statement

    :param elements: [Strings]
    :param nickname: User.nickname
    :param translator: Translator
    :return: String, Boolean
    """
    logger('ReviewQueues', 'add_proposals_for_statement_corrections', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return translator.get(_.noRights), True

    review_count = len(elements)
    added_reviews = [__add_edit_reviews(element, db_user) for element in elements]

    if added_reviews.count(1) == 0:  # no edits set
        if added_reviews.count(-1) > 0:
            logger('ReviewQueues', 'add_proposals_for_statement_corrections', 'internal key error')
            return translator.get(_.internalKeyError), True
        if added_reviews.count(-2) > 0:
            logger('ReviewQueues', 'add_proposals_for_statement_corrections', 'already edit proposals')
            return translator.get(_.alreadyEditProposals), True
        logger('ReviewQueues', 'add_proposals_for_statement_corrections', 'no corrections given')
        return translator.get(_.noCorrections), True

    DBDiscussionSession.flush()
    transaction.commit()

    added_values = [__add_edit_values_review(element, db_user) for element in elements]
    if added_values == 0:
        return translator.get(_.alreadyEditProposals), True
    DBDiscussionSession.flush()
    transaction.commit()

    msg = ''
    if review_count > added_values.count(1) or added_reviews.count(1) != added_values.count(1):
        msg = translator.get(_.alreadyEditProposals)

    return msg, False


def __add_edit_reviews(element, db_user):
    """
    Setup a new ReviewEdit row

    :param element: String
    :param db_user: User
    :return: -1 if the statement of the element does not exists, -2 if this edit already exists, 1 on success, 0 otherwise
    """
    logger('ReviewQueues', '__add_edit_reviews', 'current element: {}'.format(element))
    db_statement = DBDiscussionSession.query(Statement).get(element['uid'])
    if not db_statement:
        logger('ReviewQueues', '__add_edit_reviews', 'statement {} not found (return -1)'.format(element['uid']))
        return -1

    # already set an correction for this?
    if is_statement_in_edit_queue(element['uid']):  # if we already have an edit, skip this
        logger('ReviewQueues', '__add_edit_reviews', '{} already got an edit (return -2)'.format(element['uid']))
        return -2

    db_textversion = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)
    if len(element['text']) > 0 and db_textversion.content.lower().strip() != element['text'].lower().strip():
        logger('ReviewQueues', '__add_edit_reviews', 'added review element for {}  (return 1)'.format(element['uid']))
        DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=element['uid']))
        return 1

    return 0


def is_statement_in_edit_queue(uid):
    """
    Returns true if the statement is not in the edit queue

    :param uid: Statement.uid
    :return: Boolean
    """
    db_already_edit = DBDiscussionSession.query(ReviewEdit).filter(and_(ReviewEdit.statement_uid == uid,
                                                                        ReviewEdit.is_executed == False)).all()
    return db_already_edit and len(db_already_edit) > 0


def is_arguments_premise_in_edit_queue(uid):
    """
    Returns true if the premises of an argument are not in the edit queue

    :param uid: Argument.uid
    :return: Boolean
    """
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    db_already_edit = []
    for premise in db_premises:
        db_already_edit += DBDiscussionSession.query(ReviewEdit).filter(and_(ReviewEdit.statement_uid == premise.statement_uid,
                                                                             ReviewEdit.is_executed == False)).all()
    return db_already_edit and len(db_already_edit) > 0


def __add_edit_values_review(element, db_user):
    """
    Setup a new ReviewEditValue row

    :param element: String
    :param db_user: User
    :return: 1 on success, 0 otherwise
    """
    logger('ReviewQueues', '__add_edit_values_review', 'current element: ' + str(element))
    db_statement = DBDiscussionSession.query(Statement).get(element['uid'])
    if not db_statement:
        logger('ReviewQueues', '__add_edit_values_review', str(element['uid']) + ' not found')
        return 0

    db_textversion = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)

    if len(element['text']) > 0 and db_textversion.content.lower().strip() != element['text'].lower().strip():
        db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(and_(ReviewEdit.detector_uid == db_user.uid,
                                                                           ReviewEdit.statement_uid == element['uid'])).order_by(ReviewEdit.uid.desc()).first()
        DBDiscussionSession.add(ReviewEditValue(db_review_edit.uid, element['uid'], 'statement', element['text']))
        logger('ReviewQueues', '__add_edit_values_review', '{} - \'{}\' accepted'.format(element['uid'], element['text']))
        return 1
    else:
        logger('ReviewQueues', '__add_edit_values_review', '{} - \'{}\' malicious edit'.format(element['uid'], element['text']))
        return 0


def lock_optimization_review(nickname, review_uid, translator):
    """
    Locks a ReviewOptimization

    :param nickname: User.nickname
    :param review_uid: ReviewOptimization.uid
    :param translator: Translator
    :return: success, info, error, is_locked
    :rtype: String, String, String, Boolean
    """
    logger('ReviewQueues', 'lock_optimization_review', 'main')
    success = ''
    info = ''
    error = ''
    is_locked = False

    # has user already locked an item?
    db_user  = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_lock = DBDiscussionSession.query(ReviewOptimization).get(review_uid)

    if not db_user or int(review_uid) < 1 or not db_lock:
        logger('ReviewQueues', 'lock_optimization_review', 'no user or no review (' + str(not db_user) + ',' + str(not db_lock) + ')', error=True)
        error = translator.get(_.internalKeyError)
        return success, info, error, is_locked

    # check if author locked an item and maybe tidy up old locks
    db_locks = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).first()
    if db_locks:
        if is_review_locked(db_locks.review_optimization_uid):
            info = translator.get(_.dataAlreadyLockedByYou)
            is_locked = True
            logger('ReviewQueues', 'lock_optimization_review', 'review already locked')
            return success, info, error, is_locked
        else:
            DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).delete()

    # is already locked?
    if is_review_locked(review_uid):
        logger('ReviewQueues', 'lock_optimization_review', 'already locked', warning=True)
        info = translator.get(_.dataAlreadyLockedByOthers)
        is_locked = True
        return success, info, error, is_locked

    DBDiscussionSession.add(OptimizationReviewLocks(db_user.uid, review_uid))
    DBDiscussionSession.flush()
    transaction.commit()
    is_locked = True
    success = translator.get(_.dataAlreadyLockedByYou)

    logger('ReviewQueues', 'lock_optimization_review', 'review locked')
    return success, info, error, is_locked


def unlock_optimization_review(review_uid):
    """
    Unlock the OptimizationReviewLocks

    :param review_uid: OptimizationReviewLocks.uid
    :return: True
    """
    tidy_up_optimization_locks()
    logger('ReviewQueues', 'unlock_optimization_review', 'main')
    DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=review_uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def is_review_locked(review_uid):
    """
    Is the OptimizationReviewLocks set?

    :param review_uid: OptimizationReviewLocks.uid
    :return: Boolean
    """
    tidy_up_optimization_locks()
    logger('ReviewQueues', 'is_review_locked', 'main')
    db_lock = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=review_uid).first()
    if not db_lock:
        return False
    return (get_now() - db_lock.locked_since).seconds < max_lock_time_in_sec


def tidy_up_optimization_locks():
    """
    Tidy up all expired locks

    :return: None
    """
    logger('ReviewQueues', 'tidy_up_optimization_locks', 'main')
    db_locks = DBDiscussionSession.query(OptimizationReviewLocks).all()
    for lock in db_locks:
        if (get_now() - lock.locked_since).seconds >= max_lock_time_in_sec:
            DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=lock.review_optimization_uid).delete()
