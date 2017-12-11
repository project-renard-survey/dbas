from enum import Enum


class Keywords(Enum):
    arguments = 'arguments'
    error = 'error'
    iActuallyHave = 'iActuallyHave'
    insertOneArgument = 'insertOneArgument'
    insertDontCare = 'insertDontCare'
    forgotInputRadio = 'forgotInputRadio'
    needHelpToUnderstandStatement = 'needHelpToUnderstandStatement'
    setPremisegroupsIntro1 = 'setPremisegroupsIntro1'
    setPremisegroupsIntro2 = 'setPremisegroupsIntro2'
    attack = 'attack'
    support = 'support'
    premise = 'premise'
    because = 'because'
    moreAbout = 'moreAbout'
    undermine = 'undermine'
    support1 = 'support1'
    undercut1 = 'undercut1'
    undercut2 = 'undercut2'
    overbid1 = 'overbid1'
    overbid2 = 'overbid2'
    rebut1 = 'rebut1'
    rebut2 = 'rebut2'
    oldPwdEmpty = 'oldPwdEmpty'
    newPwdEmtpy = 'newPwdEmtpy'
    confPwdEmpty = 'confPwdEmpty'
    newPwdNotEqual = 'newPwdNotEqual'
    pwdsSame = 'pwdsSame'
    oldPwdWrong = 'oldPwdWrong'
    pwdChanged = 'pwdChanged'
    emptyName = 'emptyName'
    emptyEmail = 'emptyEmail'
    emtpyContent = 'emtpyContent'
    maliciousAntiSpam = 'maliciousAntiSpam'
    maliciousSlug = 'maliciousSlug'
    nonValidCSRF = 'nonValidCSRF'
    name = 'name'
    mail = 'mail'
    phone = 'phone'
    message = 'message'
    messageDeleted = 'messageDeleted'
    notification = 'notification'
    notificationDeleted = 'notificationDeleted'
    pwdNotEqual = 'pwdNotEqual'
    pwdShort = 'pwdShort'
    nickIsTaken = 'nickIsTaken'
    mailIsTaken = 'mailIsTaken'
    mailNotValid = 'mailNotValid'
    mailSettingsTitle = 'mailSettingsTitle'
    notificationSettingsTitle = 'notificationSettingsTitle'
    errorTryLateOrContant = 'errorTryLateOrContant'
    accountWasAdded = 'accountWasAdded'
    accountRegistration = 'accountRegistration'
    accountWasRegistered = 'accountWasRegistered'
    accoutErrorTryLateOrContant = 'accoutErrorTryLateOrContant'
    nicknameIs = 'nicknameIs'
    newPwdIs = 'newPwdIs'
    newPwdInfo = 'newPwdInfo'
    dbasPwdRequest = 'dbasPwdRequest'
    antispamquestion = 'antispamquestion'
    defaultView = 'defaultView'
    positions = 'positions'
    labels = 'labels'
    showMyPath = 'showMyPath'
    hideMyPath = 'hideMyPath'
    myStatements = 'myStatements'
    supportsOnMyStatements = 'supportsOnMyStatements'
    attacksOnMyStatements = 'attacksOnMyStatements'
    addATopic = 'addATopic'
    editIssueViewChangelog = 'editIssueViewChangelog'
    editTitleHere = 'editTitleHere'
    editInfoHere = 'editInfoHere'
    viewChangelog = 'viewChangelog'
    editStatementHere = 'editStatementHere'
    save = 'save'
    cancel = 'cancel'
    submit = 'submit'
    close = 'close'
    urlSharing = 'urlSharing'
    urlSharingDescription = 'urlSharingDescription'
    warning = 'warning'
    islandViewFor = 'islandViewFor'
    resumeHere = 'resumeHere'
    aand = 'aand'
    andor = 'andor'
    addedEverything = 'addedEverything'
    addStatementRow = 'addStatementRow'
    addTopic = 'addTopic'
    alreadyInserted = 'alreadyInserted'
    addIssueInfo = 'addIssueInfo'
    addPremisesRadioButtonText = 'addPremisesRadioButtonText'
    addArgumentsRadioButtonText = 'addArgumentsRadioButtonText'
    argumentContainerTextIfPremises = 'argumentContainerTextIfPremises'
    argumentContainerTextIfArguments = 'argumentContainerTextIfArguments'
    addPremiseRadioButtonText = 'addPremiseRadioButtonText'
    addArgumentRadioButtonText = 'addArgumentRadioButtonText'
    argumentContainerTextIfPremise = 'argumentContainerTextIfPremise'
    argumentContainerTextIfArgument = 'argumentContainerTextIfArgument'
    argumentContainerTextIfConclusion = 'argumentContainerTextIfConclusion'
    argueAgainstPositionToggleButton = 'argueAgainstPositionToggleButton'
    argueForPositionToggleButton = 'argueForPositionToggleButton'
    andIDoNotBelieveCounter = 'andIDoNotBelieveCounter'
    andIDoNotBelieveArgument = 'andIDoNotBelieveArgument'
    andTheyDoNotBelieveCounter = 'andTheyDoNotBelieveCounter'
    andTheyDoNotBelieveArgument = 'andTheyDoNotBelieveArgument'
    argumentFlaggedBecauseOfftopic = 'argumentFlaggedBecauseOfftopic'
    argumentFlaggedBecauseSpam = 'argumentFlaggedBecauseSpam'
    argumentFlaggedBecauseHarmful = 'argumentFlaggedBecauseHarmful'
    argumentFlaggedBecauseOptimization = 'argumentFlaggedBecauseOptimization'
    argumentFlaggedBecauseEdit = 'argumentFlaggedBecauseEdit'
    argumentFlaggedBecauseDuplicate = 'argumentFlaggedBecauseDuplicate'
    argumentFlaggedBecauseSplit = 'argumentFlaggedBecauseSplit'
    argumentFlaggedBecauseMerge = 'argumentFlaggedBecauseMerge'
    argument_optimization_description = 'argument_optimization_description'
    argument_offtopic_or_irrelevant_description = 'argument_offtopic_or_irrelevant_description'
    argument_statement_harmful_description = 'argument_statement_harmful_description'
    alternatively = 'alternatively'
    addArguments = 'addArguments'
    addStatements = 'addStatements'
    addArgumentsTitle = 'addArgumentsTitle'
    acceptItTitle = 'acceptItTitle'
    acceptIt = 'acceptIt'
    asReasonFor = 'asReasonFor'
    argument = 'argument'
    attackPosition = 'attackPosition'
    attackStatement = 'attackStatement'
    at = 'at'
    assertion = 'assertion'
    accept = 'accept'
    assistance = 'assistance'
    agreeToThis0 = 'agreeToThis0'
    agreeToThis1 = 'agreeToThis1'
    agreeToThis2 = 'agreeToThis2'
    attackedBy = 'attackedBy'
    attackedWith = 'attackedWith'
    agreeBecause = 'agreeBecause'
    andIDoBelieveCounterFor = 'andIDoBelieveCounterFor'
    andIDoBelieveArgument = 'andIDoBelieveArgument'
    attitudeFor = 'attitudeFor'
    alreadyFlaggedByOthers = 'alreadyFlaggedByOthers'
    alreadyFlaggedByYou = 'alreadyFlaggedByYou'
    alreadyEditProposals = 'alreadyEditProposals'
    alreadyExecuted = 'alreadyExecuted'
    breadcrumbsStart = 'breadcrumbsStart'
    breadcrumbsChoose = 'breadcrumbsChoose'
    breadcrumbsJustifyStatement = 'breadcrumbsJustifyStatement'
    breadcrumbsGetPremisesForStatement = 'breadcrumbsGetPremisesForStatement'
    breadcrumbsMoreAboutArgument = 'breadcrumbsMoreAboutArgument'
    breadcrumbsReplyForPremisegroup = 'breadcrumbsReplyForPremisegroup'
    breadcrumbsReplyForResponseOfConfrontation = 'breadcrumbsReplyForResponseOfConfrontation'
    breadcrumbsReplyForArgument = 'breadcrumbsReplyForArgument'
    bugSubmit = 'bugSubmit'
    butIDoNotBelieveCounterFor = 'butIDoNotBelieveCounterFor'
    butIDoNotBelieveArgumentFor = 'butIDoNotBelieveArgumentFor'
    butIDoNotBelieveReasonForReject = 'butIDoNotBelieveReasonForReject'
    butTheyDoNotBelieveCounter = 'butTheyDoNotBelieveCounter'
    butSheDoesNotBelieveCounter = 'butSheDoesNotBelieveCounter'
    butHeDoesNotBelieveCounter = 'butHeDoesNotBelieveCounter'
    butTheyDoNotBelieveArgument = 'butTheyDoNotBelieveArgument'
    butSheDoesNotBelieveArgument = 'butSheDoesNotBelieveArgument'
    butHeDoesNotBelieveArgument = 'butHeDoesNotBelieveArgument'
    butOtherParticipantsDontHaveOpinionRegardingYourOpinion = 'butOtherParticipantsDontHaveOpinionRegardingYourOpinion'
    butOtherParticipantsDontHaveArgument = 'butOtherParticipantsDontHaveArgument'
    butOtherParticipantsDontHaveCounterArgument = 'butOtherParticipantsDontHaveCounterArgument'
    butWhich = 'butWhich'
    butThisDoesNotRejectArgument = 'butThisDoesNotRejectArgument'
    butThisDoesNotRejectStatement = 'butThisDoesNotRejectStatement'
    but = 'but'
    butYouCounteredWithInterest = 'butYouCounteredWithInterest'
    butYouCounteredWithArgument = 'butYouCounteredWithArgument'
    butYouAgreedWith = 'butYouAgreedWith'
    canYouGiveAReason = 'canYouGiveAReason'
    canYouGiveAReasonFor = 'canYouGiveAReasonFor'
    canYouGiveACounter = 'canYouGiveACounter'
    canYouGiveACounterArgumentWhy1 = 'canYouGiveACounterArgumentWhy1'
    canYouGiveACounterArgumentWhy2 = 'canYouGiveACounterArgumentWhy2'
    canYouGiveAReasonForThat = 'canYouGiveAReasonForThat'
    canYouBeMorePrecise = 'canYouBeMorePrecise'
    clickHereForRegistration = 'clickHereForRegistration'
    clickForMore = 'clickForMore'
    countOfArguments = 'countOfArguments'
    countOfPosts = 'countOfPosts'
    confirmation = 'confirmation'
    contact = 'contact'
    contactSubmit = 'contactSubmit'
    confirmTranslation = 'confirmTranslation'
    correctionsSet = 'correctionsSet'
    checkFirstname = 'checkFirstname'
    checkLastname = 'checkLastname'
    checkNickname = 'checkNickname'
    checkEmail = 'checkEmail'
    checkPassword = 'checkPassword'
    checkConfirmation = 'checkConfirmation'
    completeView = 'completeView'
    completeViewTitle = 'completeViewTitle'
    checkPasswordConfirm = 'checkPasswordConfirm'
    clickToChoose = 'clickToChoose'
    clearStatistics = 'clearStatistics'
    congratulation = 'congratulation'
    currentDiscussion = 'currentDiscussion'
    description_undermine = 'description_undermine'
    description_support = 'description_support'
    description_undercut = 'description_undercut'
    description_overbid = 'description_overbid'
    description_rebut = 'description_rebut'
    description_no_opinion = 'description_no_opinion'
    decisionIndex7 = 'decisionIndex7'
    decisionIndex30 = 'decisionIndex30'
    decisionIndex7Info = 'decisionIndex7Info'
    decisionIndex30Info = 'decisionIndex30Info'
    dateString = 'dateString'
    deleteTrack = 'deleteTrack'
    deleteStatement = 'deleteStatement'
    disassociateStatement = 'disassociateStatement'
    deleteHistory = 'deleteHistory'
    delete = 'delete'
    disagreeBecause = 'disagreeBecause'
    dataRemoved = 'dataRemoved'
    didYouMean = 'didYouMean'
    dialogView = 'dialogView'
    dialogViewTitle = 'dialogViewTitle'
    displayControlDialogGuidedTitle = 'displayControlDialogGuidedTitle'
    displayControlDialogGuidedBody = 'displayControlDialogGuidedBody'
    displayControlDialogIslandTitle = 'displayControlDialogIslandTitle'
    displayControlDialogIslandBody = 'displayControlDialogIslandBody'
    displayControlDialogExpertTitle = 'displayControlDialogExpertTitle'
    displayControlDialogExpertBody = 'displayControlDialogExpertBody'
    displayControlDialogGraphTitle = 'displayControlDialogGraphTitle'
    displayControlDialogGraphBody = 'displayControlDialogGraphBody'
    discussionEnd = 'discussionEnd'
    discussionCongratulationEnd = 'discussionCongratulationEnd'
    discussionEndLinkTextLoggedIn = 'discussionEndLinkTextLoggedIn'
    discussionEndLinkTextNotLoggedIn = 'discussionEndLinkTextNotLoggedIn'
    discussionEndLinkTextWithQueueLoggedIn = 'discussionEndLinkTextWithQueueLoggedIn'
    discussionEndLinkTextWithQueueNotLoggedIn = 'discussionEndLinkTextWithQueueNotLoggedIn'
    discussionInfoTooltip1 = 'discussionInfoTooltip1'
    discussionInfoTooltip2 = 'discussionInfoTooltip2'
    discussionInfoTooltip3sg = 'discussionInfoTooltip3sg'
    discussionInfoTooltip3pl = 'discussionInfoTooltip3pl'
    discussionIsReadOnly = 'discussionIsReadOnly'
    disagreeToThis0 = 'disagreeToThis0'
    disagreeToThis1 = 'disagreeToThis1'
    disagreeToThis2 = 'disagreeToThis2'
    duplicate = 'duplicate'
    duplicateDialog = 'duplicateDialog'
    doesNotHold = 'doesNotHold'
    isNotRight = 'isNotRight'
    isNoGoodJustification = 'isNoGoodJustification'
    doNotHesitateToContact = 'doNotHesitateToContact'
    docs = 'docs'
    doesJustify = 'doesJustify'
    doesNotJustify = 'doesNotJustify'
    doYouWantToEnterYourStatements = 'doYouWantToEnterYourStatements'
    dataNowLocked = 'dataNowLocked'
    dataUnlocked = 'dataUnlocked'
    dataAlreadyLockedByYou = 'dataAlreadyLockedByYou'
    dataAlreadyLockedByOthers = 'dataAlreadyLockedByOthers'
    earlierYouArguedThat = 'earlierYouArguedThat'
    eachStatement = 'eachStatement'
    editIndex = 'editIndex'
    editIndexInfo = 'editIndexInfo'
    euCookiePopupTitle = 'euCookiePopupTitle'
    euCookiePopupText = 'euCookiePopupText'
    euCookiePopoupButton1 = 'euCookiePopoupButton1'
    euCookiePopoupButton2 = 'euCookiePopoupButton2'
    empty_news_input = 'empty_news_input'
    empty_notification_input = 'empty_notification_input'
    email = 'email'
    emailWasSent = 'emailWasSent'
    emailWasNotSent = 'emailWasNotSent'
    emailUnknown = 'emailUnknown'
    emailBodyText = 'emailBodyText'
    emailArgumentAddTitle = 'emailArgumentAddTitle'
    emailArgumentAddBody = 'emailArgumentAddBody'
    exampleName = 'exampleName'
    exampleMail = 'exampleMail'
    examplePhone = 'examplePhone'
    exampleMessage = 'exampleMessage'
    exampleMessageBug = 'exampleMessageBug'
    exampleNickname = 'exampleNickname'
    examplePassword = 'examplePassword'
    exampleNicknameLdap = 'exampleNicknameLdap'
    exampleFirstname = 'exampleFirstname'
    exampleLastname = 'exampleLastname'
    exampleStatement = 'exampleStatement'
    exampleSource = 'exampleSource'
    exampleSearchDuplicate = 'exampleSearchDuplicate'
    examplePosition = 'examplePosition'
    exampleReason = 'exampleReason'
    exampleAddTopicTitle = 'exampleAddTopicTitle'
    exampleAddTopicQuestion = 'exampleAddTopicQuestion'
    exampleAddTopicDescription = 'exampleAddTopicDescription'
    everythingSaved = 'everythingSaved'
    opinionSaved = 'opinionSaved'
    error_code = 'error_code'
    edit = 'edit'
    editTitle = 'editTitle'
    editAlreadyTitle = 'editAlreadyTitle'
    feelFreeToLogin = 'feelFreeToLogin'
    forText = 'forText'
    forThat = 'forThat'
    firstConclusionRadioButtonText = 'firstConclusionRadioButtonText'
    firstArgumentRadioButtonText = 'firstArgumentRadioButtonText'
    feelFreeToShareUrl = 'feelFreeToShareUrl'
    fetchLongUrl = 'fetchLongUrl'
    fetchShortUrl = 'fetchShortUrl'
    forgotPassword = 'forgotPassword'
    firstOneInformationText = 'firstOneInformationText'
    firstOneInformationTextM = 'firstOneInformationTextM'
    firstOneInformationTextF = 'firstOneInformationTextF'
    firstOneReason = 'firstOneReason'
    firstOneReasonM = 'firstOneReasonM'
    firstOneReasonF = 'firstOneReasonF'
    firstPositionText = 'firstPositionText'
    firstPositionTextM = 'firstPositionTextM'
    firstPositionTextF = 'firstPositionTextF'
    firstPremiseText1 = 'firstPremiseText1'
    firstPremiseText1M = 'firstPremiseText1M'
    firstPremiseText1F = 'firstPremiseText1F'
    firstPremiseText2 = 'firstPremiseText2'
    firstname = 'firstname'
    fillLine = 'fillLine'
    finish = 'finish'
    finishTitle = 'finishTitle'
    fieldtest = 'fieldtest'
    fromm = 'fromm'
    gender = 'gender'
    goBack = 'goBack'
    goHome = 'goHome'
    goStepBack = 'goStepBack'
    generateSecurePassword = 'generateSecurePassword'
    goodPointTakeMeBackButtonText = 'goodPointTakeMeBackButtonText'
    group_uid = 'group_uid'
    goBackToTheDiscussion = 'goBackToTheDiscussion'
    goForward = 'goForward'
    goodPointAndUserIsInterestedTooM = 'goodPointAndUserIsInterestedTooM'
    goodPointAndUserIsInterestedTooF = 'goodPointAndUserIsInterestedTooF'
    goodPointAndOtherParticipantsIsInterestedToo = 'goodPointAndOtherParticipantsIsInterestedToo'
    haveALookAt = 'haveALookAt'
    hidePasswordRequest = 'hidePasswordRequest'
    hideGenerator = 'hideGenerator'
    hold = 'hold'
    howeverIHaveMuchStrongerArgumentRejectingThat = 'howeverIHaveMuchStrongerArgumentRejectingThat'
    howeverIHaveMuchStrongerArgumentAcceptingThat = 'howeverIHaveMuchStrongerArgumentAcceptingThat'
    howeverIHaveMuchStrongerArgument = 'howeverIHaveMuchStrongerArgument'
    howeverIHaveMuchStrongerArgumentTo = 'howeverIHaveMuchStrongerArgumentTo'
    howeverIHaveEvenStrongerArgumentRejecting = 'howeverIHaveEvenStrongerArgumentRejecting'
    howeverIHaveEvenStrongerArgumentAccepting = 'howeverIHaveEvenStrongerArgumentAccepting'
    imprint = 'imprint'
    iAgreeWithInColor = 'iAgreeWithInColor'
    iAgreeWith = 'iAgreeWith'
    iDisagreeWithInColor = 'iDisagreeWithInColor'
    iDisagreeWith = 'iDisagreeWith'
    iDoNotKnow = 'iDoNotKnow'
    iDoNotKnowInColor = 'iDoNotKnowInColor'
    iHaveNoOpinionYet = 'iHaveNoOpinionYet'
    iHaveNoOpinion = 'iHaveNoOpinion'
    iHaveNoOpinionYetInColor = 'iHaveNoOpinionYetInColor'
    informationForExperts = 'informationForExperts'
    internalFailureWhileDeletingTrack = 'internalFailureWhileDeletingTrack'
    internalFailureWhileDeletingHistory = 'internalFailureWhileDeletingHistory'
    internalError = 'internalError'
    internalErrorHTTPS = 'internalErrorHTTPS'
    internalKeyError = 'internalKeyError'
    issueList = 'issueList'
    islandViewHeaderText = 'islandViewHeaderText'
    islandView = 'islandView'
    islandViewTitle = 'islandViewTitle'
    irrelevant = 'irrelevant'
    itIsTrueThat = 'itIsTrueThat'
    maybeItIsTrueThat = 'maybeItIsTrueThat'
    itIsTrueThatAnonymous = 'itIsTrueThatAnonymous'
    itIsTrue1 = 'itIsTrue1'
    itIsTrue2 = 'itIsTrue2'
    itIsFalseThat = 'itIsFalseThat'
    itIsFalseThatAnonymous = 'itIsFalseThatAnonymous'
    itIsFalse1 = 'itIsFalse1'
    itIsFalse2 = 'itIsFalse2'
    itTrueIsThat = 'itTrueIsThat'
    itFalseIsThat = 'itFalseIsThat'
    isFalse = 'isFalse'
    isNotAGoodIdea = 'isNotAGoodIdea'
    isNotAGoodReasonFor = 'isNotAGoodReasonFor'
    isNotAGoodReasonAgainstArgument = 'isNotAGoodReasonAgainstArgument'
    issueEnableDescription = 'issueEnableDescription'
    issuePublicDescription = 'issuePublicDescription'
    issueWritableDescription = 'issueWritableDescription'
    itIsNotRight = 'itIsNotRight'
    isNotAGoodIdeaInColor = 'isNotAGoodIdeaInColor'
    isTrue = 'isTrue'
    areTrue = 'areTrue'
    initialPositionInterest = 'initialPositionInterest'
    invalidEmail = 'invalidEmail'
    iAcceptCounter = 'iAcceptCounter'
    iAcceptArgument = 'iAcceptArgument'
    iAcceptCounterThat = 'iAcceptCounterThat'
    iAcceptArgumentThat = 'iAcceptArgumentThat'
    iHaveMuchStrongerArgumentRejecting = 'iHaveMuchStrongerArgumentRejecting'
    iHaveEvenStrongerArgumentRejecting = 'iHaveEvenStrongerArgumentRejecting'
    iHaveMuchStrongerArgumentAccepting = 'iHaveMuchStrongerArgumentAccepting'
    iHaveEvenStrongerArgumentAccepting = 'iHaveEvenStrongerArgumentAccepting'
    iNoOpinion = 'iNoOpinion'
    interestingOnDBAS = 'interestingOnDBAS'
    inputEmpty = 'inputEmpty'
    informationForStatements = 'informationForStatements'
    relativePopularityOfStatements = 'relativePopularityOfStatements'
    jumpAnswer0 = 'jumpAnswer0'
    jumpAnswer1 = 'jumpAnswer1'
    jumpAnswer2 = 'jumpAnswer2'
    jumpAnswer3 = 'jumpAnswer3'
    jumpAnswer4 = 'jumpAnswer4'
    supportAnswer0 = 'supportAnswer0'
    supportAnswer1 = 'supportAnswer1'
    supportAnswer2 = 'supportAnswer2'
    supportAnswer3 = 'supportAnswer3'
    justLookDontTouch = 'justLookDontTouch'
    keyword = 'keyword'
    keywordStart = 'keywordStart'
    keywordChooseActionForStatement = 'keywordChooseActionForStatement'
    keywordGetPremisesForStatement = 'keywordGetPremisesForStatement'
    keywordMoreAboutArgument = 'keywordMoreAboutArgument'
    keywordReplyForPremisegroup = 'keywordReplyForPremisegroup'
    keywordReplyForResponseOfConfrontation = 'keywordReplyForResponseOfConfrontation'
    keywordReplyForArgument = 'keywordReplyForArgument'
    keepSetting = 'keepSetting'
    holds = 'holds'
    holdsInColor = 'holdsInColor'
    hideAllUsers = 'hideAllUsers'
    hideAllAttacks = 'hideAllAttacks'
    letMeExplain = 'letMeExplain'
    levenshteinDistance = 'levenshteinDistance'
    languageCouldNotBeSwitched = 'languageCouldNotBeSwitched'
    last_action = 'last_action'
    last_login = 'last_login'
    login = 'login'
    logfile = 'logfile'
    letsGo = 'letsGo'
    letsGoBack = 'letsGoBack'
    letsGoHome = 'letsGoHome'
    langNotFound = 'langNotFound'
    latestNewsFromDiscussion = 'latestNewsFromDiscussion'
    latestNewsFromDBAS = 'latestNewsFromDBAS'
    ldapInfo = 'ldapInfo'
    more = 'more'
    medium = 'medium'
    minLength = 'minLength'
    myArgument = 'myArgument'
    mark_as_opinion = 'mark_as_opinion'
    unmark_as_opinion = 'unmark_as_opinion'
    next = 'next'
    now = 'now'
    nowYouSayThat = 'nowYouSayThat'
    newNotification = 'newNotification'
    newMention = 'newMention'
    newPremiseRadioButtonText = 'newPremiseRadioButtonText'
    newPremiseRadioButtonTextAsFirstOne = 'newPremiseRadioButtonTextAsFirstOne'
    newConclusionRadioButtonText = 'newConclusionRadioButtonText'
    newConclusionRadioButtonTextNewIdea = 'newConclusionRadioButtonTextNewIdea'
    newsAboutDbas = 'newsAboutDbas'
    nickname = 'nickname'
    noOtherAttack = 'noOtherAttack'
    noIslandView = 'noIslandView'
    noCorrections = 'noCorrections'
    noCorrectionsSet = 'noCorrectionsSet'
    noDecisionDone = 'noDecisionDone'
    noDataSelected = 'noDataSelected'
    notInsertedErrorBecauseEmpty = 'notInsertedErrorBecauseEmpty'
    notInsertedErrorBecauseDuplicate = 'notInsertedErrorBecauseDuplicate'
    notInsertedErrorBecauseUnknown = 'notInsertedErrorBecauseUnknown'
    notInsertedErrorBecauseInternal = 'notInsertedErrorBecauseInternal'
    noEntries = 'noEntries'
    noTrackedData = 'noTrackedData'
    number = 'number'
    note = 'note'
    no_entry = 'no_entry'
    no_arguments = 'no_arguments'
    noRights = 'noRights'
    notLoggedIn = 'notLoggedIn'
    on = 'on'
    of = 'of'
    off = 'off'
    opinion_his = 'opinion_his'
    opinion_her = 'opinion_her'
    opinion = 'opinion'
    onlyOneItem = 'onlyOneItem'
    onlyOneItemWithLink = 'onlyOneItemWithLink'
    unfortunatelyOnlyOneItem = 'unfortunatelyOnlyOneItem'
    otherParticipantsConvincedYouThat = 'otherParticipantsConvincedYouThat'
    otherParticipantsThinkThat = 'otherParticipantsThinkThat'
    otherParticipantsAgreeThat = 'otherParticipantsAgreeThat'
    thinkThat = 'thinkThat'
    agreeThat = 'agreeThat'
    thinksThat = 'thinksThat'
    agreesThat = 'agreesThat'
    that = 'that'
    earlierYouHadNoOpinitionForThisStatement = 'earlierYouHadNoOpinitionForThisStatement'
    otherUserDoesntHaveOpinionForThisStatement = 'otherUserDoesntHaveOpinionForThisStatement'
    otherParticipantsDontHaveOpinionForThisStatement = 'otherParticipantsDontHaveOpinionForThisStatement'
    otherParticipantsDontHaveOpinion = 'otherParticipantsDontHaveOpinion'
    otherParticipantsDontHaveOpinionRegaringYourSelection = 'otherParticipantsDontHaveOpinionRegaringYourSelection'
    otherParticipantsDontHaveCounterForThat = 'otherParticipantsDontHaveCounterForThat'
    otherParticipantsDontHaveNewCounterForThat = 'otherParticipantsDontHaveNewCounterForThat'
    otherParticipantsDontHaveCounter = 'otherParticipantsDontHaveCounter'
    otherParticipantsDontHaveArgument = 'otherParticipantsDontHaveArgument'
    otherParticipantsAcceptBut = 'otherParticipantsAcceptBut'
    otherParticipantDisagreeThat = 'otherParticipantDisagreeThat'
    otherUsersClaimStrongerArgumentS = 'otherUsersClaimStrongerArgumentS'
    otherUsersClaimStrongerArgumentP = 'otherUsersClaimStrongerArgumentP'
    claimsStrongerArgumentRejecting = 'claimsStrongerArgumentRejecting'
    claimsStrongerArgumentAccepting = 'claimsStrongerArgumentAccepting'
    otherUsersHaveCounterArgument = 'otherUsersHaveCounterArgument'
    otherUsersSaidThat = 'otherUsersSaidThat'
    thenOtherUsersSaidThat = 'thenOtherUsersSaidThat'
    opinionBarometer = 'opinionBarometer'
    pleaseAddYourSuggestion = 'pleaseAddYourSuggestion'
    pleaseTryAgainLaterOrContactUs = 'pleaseTryAgainLaterOrContactUs'
    premiseGroup = 'premiseGroup'
    premisegroupPopupWarning = 'premisegroupPopupWarning'
    previous = 'previous'
    publicNickTitle = 'publicNickTitle'
    passwordSubmit = 'passwordSubmit'
    preferedLangTitle = 'preferedLangTitle'
    priv_access_opti_queue = 'priv_access_opti_queue'
    priv_access_del_queue = 'priv_access_del_queue'
    priv_access_edit_queue = 'priv_access_edit_queue'
    priv_access_duplicate_queue = 'priv_access_duplicate_queue'
    priv_access_splits_queue = 'priv_access_splits_queue'
    priv_access_merges_queue = 'priv_access_merges_queue'
    priv_history_queue = 'priv_history_queue'
    publications = 'publications'
    queueDelete = 'queueDelete'
    queueOptimization = 'queueOptimization'
    queueEdit = 'queueEdit'
    queueDuplicates = 'queueDuplicates'
    queueSplit = 'queueSplit'
    queueMerge = 'queueMerge'
    queueHistory = 'queueHistory'
    queueOngoing = 'queueOngoing'
    requestPassword = 'requestPassword'
    myPosition = 'myPosition'
    myPositionGenitiv = 'myPositionGenitiv'
    the_der = 'the_der'
    the_die = 'the_die'
    the_das = 'the_das'
    reference = 'reference'
    registered = 'registered'
    restartDiscussion = 'restartDiscussion'
    restartDiscussionTitle = 'restartDiscussionTitle'
    restartOnError = 'restartOnError'
    recipient = 'recipient'
    recipientNotFound = 'recipientNotFound'
    report = 'report'
    reportStatement = 'reportStatement'
    reportArgument = 'reportArgument'
    reportIssue = 'reportIssue'
    review = 'review'
    review_history = 'review_history'
    review_ongoing = 'review_ongoing'
    reputation = 'reputation'
    right = 'right'
    reason = 'reason'
    requestTrack = 'requestTrack'
    refreshTrack = 'refreshTrack'
    requestHistory = 'requestHistory'
    refreshHistory = 'refreshHistory'
    requestFailed = 'requestFailed'
    reject = 'reject'
    rejection = 'rejection'
    remStatementRow = 'remStatementRow'
    reaction = 'reaction'
    attitudesOfOpinions = 'attitudesOfOpinions'
    reactionFor = 'reactionFor'
    agreeVsDisagree = 'agreeVsDisagree'
    rep_reason_first_argument_click = 'rep_reason_first_argument_click'
    rep_reason_first_confrontation = 'rep_reason_first_confrontation'
    rep_reason_first_position = 'rep_reason_first_position'
    rep_reason_first_justification = 'rep_reason_first_justification'
    rep_reason_first_new_argument = 'rep_reason_first_new_argument'
    rep_reason_new_statement = 'rep_reason_new_statement'
    rep_reason_success_flag = 'rep_reason_success_flag'
    rep_reason_success_edit = 'rep_reason_success_edit'
    rep_reason_success_duplicate = 'rep_reason_success_duplicate'
    rep_reason_bad_flag = 'rep_reason_bad_flag'
    rep_reason_bad_edit = 'rep_reason_bad_edit'
    rep_reason_bad_duplicate = 'rep_reason_bad_duplicate'
    reaction_text_undermine = 'reaction_text_undermine'
    reaction_text_support = 'reaction_text_support'
    reaction_text_undercut = 'reaction_text_undercut'
    reaction_text_undercut_for_dont_know = 'reaction_text_undercut_for_dont_know'
    reaction_text_rebut = 'reaction_text_rebut'
    reaction_text_rebut_for_dont_know = 'reaction_text_rebut_for_dont_know'
    questionTitle = 'questionTitle'
    saveMyStatement = 'saveMyStatement'
    selectStatement = 'selectStatement'
    selectMultipleStatementsWhichFlag = 'selectMultipleStatementsWhichFlag'
    mergeStatement = 'mergeStatement'
    mergeMultipleStatements = 'mergeMultipleStatements'
    mergeMultiplePGroup = 'mergeMultiplePGroup'
    splitStatement = 'splitStatement'
    splitMultipleStatements = 'splitMultipleStatements'
    splitMultiplePGroup = 'splitMultiplePGroup'
    showAllUsers = 'showAllUsers'
    showAllArguments = 'showAllArguments'
    showAllArgumentsTitle = 'showAllArgumentsTitle'
    showAllUsersTitle = 'showAllUsersTitle'
    supportPosition = 'supportPosition'
    supportsNot = 'supportsNot'
    isupport = 'isupport'
    strength = 'strength'
    strong = 'strong'
    strongerStatementF = 'strongerStatementF'
    strongerStatementM = 'strongerStatementM'
    strongerStatementP = 'strongerStatementP'
    strongerStatementY = 'strongerStatementY'
    accepting = 'accepting'
    rejecting = 'rejecting'
    strongerStatementEnd = 'strongerStatementEnd'
    search = 'search'
    searchForStatements = 'searchForStatements'
    serviceNotAvailable = 'serviceNotAvailable'
    someoneArgued = 'someoneArgued'
    soYouEnteredMultipleReasons = 'soYouEnteredMultipleReasons'
    soYourOpinionIsThat = 'soYourOpinionIsThat'
    soYouWantToArgueAgainst = 'soYouWantToArgueAgainst'
    shortenedBy = 'shortenedBy'
    shareUrl = 'shareUrl'
    showMeAnotherArgument = 'showMeAnotherArgument'
    switchDiscussion = 'switchDiscussion'
    switchDiscussionTitle = 'switchDiscussionTitle'
    switchDiscussionText1 = 'switchDiscussionText1'
    switchDiscussionText2 = 'switchDiscussionText2'
    switchLanguage = 'switchLanguage'
    statement = 'statement'
    statementAdded = 'statementAdded'
    statementIsAbout = 'statementIsAbout'
    statementAbout = 'statementAbout'
    statementIsDuplicate = 'statementIsDuplicate'
    statement_offtopic_or_irrelevant_description = 'statement_offtopic_or_irrelevant_description'
    statement_duplicate_description = 'statement_duplicate_description'
    statement_merge_description = 'statement_merge_description'
    statement_split_description = 'statement_split_description'
    statement_optimization_description = 'statement_optimization_description'
    settings = 'settings'
    senderReceiverSame = 'senderReceiverSame'
    seperated = 'seperated'
    argumentAdded = 'argumentAdded'
    positionAdded = 'positionAdded'
    statementAddedMessageContent = 'statementAddedMessageContent'
    argumentAddedMessageContent = 'argumentAddedMessageContent'
    statementIndex = 'statementIndex'
    statementIndexInfo = 'statementIndexInfo'
    statementsShowAll = 'statementsShowAll'
    statementsHideAll = 'statementsHideAll'
    sureThat = 'sureThat'
    surname = 'surname'
    myStatement = 'myStatement'
    myDiscussions = 'myDiscussions'
    showMeAnArgumentFor = 'showMeAnArgumentFor'
    textAreaReasonHintText = 'textAreaReasonHintText'
    theCounterArgument = 'theCounterArgument'
    therefore = 'therefore'
    thinkWeShould = 'thinkWeShould'
    track = 'track'
    this = 'this'
    textversionChangedTopic = 'textversionChangedTopic'
    textversionChangedContent = 'textversionChangedContent'
    to = 'to'
    history = 'history'
    topicString = 'topicString'
    text = 'text'
    theySay = 'theySay'
    heSays = 'heSays'
    sheSays = 'sheSays'
    theyThink = 'theyThink'
    participantsThink = 'participantsThink'
    heThinks = 'heThinks'
    sheThinks = 'sheThinks'
    thisIsACopyOfMail = 'thisIsACopyOfMail'
    thisConfrontationIs = 'thisConfrontationIs'
    thisArgument = 'thisArgument'
    theirArgument = 'theirArgument'
    hisArgument = 'hisArgument'
    herArgument = 'herArgument'
    theirStatement = 'theirStatement'
    hisStatement = 'hisStatement'
    herStatement = 'herStatement'
    theirAssertion = 'theirAssertion'
    herAssertion = 'herAssertion'
    hisAssertion = 'hisAssertion'
    theirPosition = 'theirPosition'
    hisPosition = 'hisPosition'
    herPosition = 'herPosition'
    theirReason = 'theirReason'
    herReason = 'herReason'
    hisReason = 'hisReason'
    textChange = 'textChange'
    thxForFlagText = 'thxForFlagText'
    veryweak = 'veryweak'
    wantToStateNewPosition = 'wantToStateNewPosition'
    weak = 'weak'
    wrong = 'wrong'
    where = 'where'
    wouldYourShareArgument = 'wouldYourShareArgument'
    whatDoYouThinkAbout = 'whatDoYouThinkAbout'
    whatDoYouThinkArgument = 'whatDoYouThinkArgument'
    whatDoYouThinkOf = 'whatDoYouThinkOf'
    whatDoYouThinkAboutThat = 'whatDoYouThinkAboutThat'
    whatIsYourIdea = 'whatIsYourIdea'
    whatIsYourMostImportantReasonForArgument = 'whatIsYourMostImportantReasonForArgument'
    whatIsYourMostImportantReasonForStatement = 'whatIsYourMostImportantReasonForStatement'
    whatIsYourMostImportantReasonAgainstArgument = 'whatIsYourMostImportantReasonAgainstArgument'
    whatIsYourMostImportantReasonAgainstStatement = 'whatIsYourMostImportantReasonAgainstStatement'
    whatIsYourMostImportantReasonWhyFor = 'whatIsYourMostImportantReasonWhyFor'
    whatIsYourMostImportantReasonWhyAgainst = 'whatIsYourMostImportantReasonWhyAgainst'
    whatIsYourMostImportantReasonWhyForInColor = 'whatIsYourMostImportantReasonWhyForInColor'
    whatIsYourMostImportantReasonWhyAgainstInColor = 'whatIsYourMostImportantReasonWhyAgainstInColor'
    whyDoYouThinkThat = 'whyDoYouThinkThat'
    wrongURL = 'wrongURL'
    whyAreYouDisagreeingWith = 'whyAreYouDisagreeingWith'
    whyAreYouAgreeingWith = 'whyAreYouAgreeingWith'
    whyAreYouDisagreeingWithInColor = 'whyAreYouDisagreeingWithInColor'
    whyAreYouAgreeingWithInColor = 'whyAreYouAgreeingWithInColor'
    whyAreYouDisagreeingWithThat = 'whyAreYouDisagreeingWithThat'
    itsYou = 'itsYou'
    youMadeA = 'youMadeA'
    youMadeAn = 'youMadeAn'
    youHaveSelectedStatement = 'youHaveSelectedStatement'
    relation_undermine = 'relation_undermine'
    relation_support = 'relation_support'
    relation_undercut = 'relation_undercut'
    relation_overbid = 'relation_overbid'
    relation_rebut = 'relation_rebut'
    uid = 'uid'
    unfortunatelyNoMoreArgument = 'unfortunatelyNoMoreArgument'
    userPasswordNotMatch = 'userPasswordNotMatch'
    userOptions = 'userOptions'
    userNotFound = 'userNotFound'
    userIsOAuth = 'userIsOAuth'
    userIsNotAuthorOfStatement = 'userIsNotAuthorOfStatement'
    userIsNotAuthorOfArgument = 'userIsNotAuthorOfArgument'
    untilNowThereAreNoMoreInformation = 'untilNowThereAreNoMoreInformation'
    voteCountTextFirst = 'voteCountTextFirst'
    voteCountTextFirstM = 'voteCountTextFirstM'
    voteCountTextFirstF = 'voteCountTextFirstF'
    voteCountTextMayBeFirst = 'voteCountTextMayBeFirst'
    voteCountTextMayBeFirstM = 'voteCountTextMayBeFirstM'
    voteCountTextMayBeFirstF = 'voteCountTextMayBeFirstF'
    voteCountTextOneOther = 'voteCountTextOneOther'
    voteCountTextOneOtherM = 'voteCountTextOneOtherM'
    voteCountTextOneOtherF = 'voteCountTextOneOtherF'
    voteCountTextMore = 'voteCountTextMore'
    voteCountTextOneMore = 'voteCountTextOneMore'
    voteCountTextOneMoreM = 'voteCountTextOneMoreM'
    voteCountTextOneMoreF = 'voteCountTextOneMoreF'
    visitDeleteQueue = 'visitDeleteQueue'
    visitDeleteQueueLimitation = 'visitDeleteQueueLimitation'
    visitEditQueue = 'visitEditQueue'
    visitEditQueueLimitation = 'visitEditQueueLimitation'
    visitDuplicateQueue = 'visitDuplicateQueue'
    visitDuplicateQueueLimitation = 'visitDuplicateQueueLimitation'
    visitOptimizationQueue = 'visitOptimizationQueue'
    visitOptimizationQueueLimitation = 'visitOptimizationQueueLimitation'
    visitSplitQueue = 'visitSplitQueue'
    visitSplitQueueLimitation = 'visitSplitQueueLimitation'
    visitMergeQueue = 'visitMergeQueue'
    visitMergeQueueLimitation = 'visitMergeQueueLimitation'
    visitHistoryQueue = 'visitHistoryQueue'
    visitHistoryQueueLimitation = 'visitHistoryQueueLimitation'
    visitOngoingQueue = 'visitOngoingQueue'
    welcome = 'welcome'
    welcomeMessage = 'welcomeMessage'
    youAreInterestedIn = 'youAreInterestedIn'
    youHaveTheOpinionThat = 'youHaveTheOpinionThat'
    youAgreeWith = 'youAgreeWith'
    youAgreeWithThatNow = 'youAgreeWithThatNow'
    youDisagreeWith = 'youDisagreeWith'
    youSaidThat = 'youSaidThat'
    youUsedThisEarlier = 'youUsedThisEarlier'
    youRejectedThisEarlier = 'youRejectedThisEarlier'
    youHaveMuchStrongerArgumentForAccepting = 'youHaveMuchStrongerArgumentForAccepting'
    youHaveMuchStrongerArgumentForRejecting = 'youHaveMuchStrongerArgumentForRejecting'
    youAreAbleToReviewNow = 'youAreAbleToReviewNow'
    youArgue = 'youArgue'
    youAgreeWithThecounterargument = 'youAgreeWithThecounterargument'

    @staticmethod
    def get_key_by_string(string):
        """
        Returns a key by his name

        :raises KeyError if the key is not in the enumeration

        :param string: The name of the key
        :return: The key
        """
        for key in Keywords:
            if key.name == string:
                return key

        raise KeyError('Invalid key: {}'.format(string))
