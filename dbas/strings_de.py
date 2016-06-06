#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


class GermanDict:

	@staticmethod
	def set_up(_self):
		"""
		Sets up the german dictionary

		:param _self:
		:return: dictionary for the german language
		"""

		de_lang = dict()

		de_lang[_self.arguments] = 'Argumente'
		de_lang[_self.error] = 'Fehler'
		de_lang[_self.iActuallyHave] = 'Ich habe'
		de_lang[_self.insertOneArgument] = 'Ich habe eine Aussage:'
		de_lang[_self.insertDontCare] = 'Es ist mir egal. Nimm\' meine Aussage wie sie ist!'
		de_lang[_self.forgotInputRadio] = 'Sie haben eine Auswahl vergessen'
		de_lang[_self.needHelpToUnderstandStatement] = 'Wir brauchen Hilfe zum Verständniss Ihrer Aussage!'
		de_lang[_self.setPremisegroupsIntro1] = 'Sie haben \'und\' in Ihrer Aussage '
		de_lang[_self.setPremisegroupsIntro2] = ' benutzt. Daher existieren mehrere mögliche Auswertungen. Bitte helfen Sie uns, die richtig Eingabe zu wählen:'

		de_lang[_self.attack] = 'Sie lehnen ab, dass'
		de_lang[_self.support] = 'Sie akzeptieren'
		de_lang[_self.premise] = 'Prämisse'
		de_lang[_self.because] = 'weil'
		de_lang[_self.moreAbout] = 'Mehr über'
		de_lang[_self.undermine] = 'Es ist falsch, dass'
		de_lang[_self.support1] = 'Es ist richtig, dass'
		de_lang[_self.undercut1] = 'Es ist falsch, dass'
		de_lang[_self.undercut2] = 'und das ist ein schlechter Konter'
		de_lang[_self.overbid1] = 'Es ist falsch, dass'
		de_lang[_self.overbid2] = 'und das ist ein guter Konter'
		de_lang[_self.rebut1] = 'Es ist richtig, dass'
		de_lang[_self.rebut2] = ', aber ich habe etwas besseres'
		de_lang[_self.oldPwdEmpty] = 'Altes Passwortfeld ist leer.'
		de_lang[_self.newPwdEmtpy] = 'Neues Passwortfeld ist leer.'
		de_lang[_self.confPwdEmpty] = 'Bestätigungs-Passwordfeld ist leer.'
		de_lang[_self.newPwdNotEqual] = 'Password und Bestätigung stimmen nicht überein.'
		de_lang[_self.pwdsSame] = 'Beide eingegeben Passwörter sind identisch.'
		de_lang[_self.oldPwdWrong] = 'Ihr altes Passwort ist falsch.'
		de_lang[_self.pwdChanged] = 'Ihr Passwort würde geändert.'
		de_lang[_self.emptyName] = 'Ihr Name ist leer!'
		de_lang[_self.emptyEmail] = 'Ihre E-Mail ist leer!'
		de_lang[_self.emtpyContent] = 'Ihr Inhalt ist leer!'
		de_lang[_self.maliciousAntiSpam] = 'Ihr Anti-Spam-Nachricht ist leer oder falsch!'
		de_lang[_self.nonValidCSRF] = 'CSRF-Token ist nicht valide'
		de_lang[_self.name] = 'Name'
		de_lang[_self.mail] = 'Mail'
		de_lang[_self.phone] = 'Telefon'
		de_lang[_self.message] = 'Nachricht'
		de_lang[_self.messageDeleted] = 'Nachricht gelöscht'
		de_lang[_self.notification] = 'Benachrichtigung'
		de_lang[_self.notificationDeleted] = 'Benachrichtigung gelöscht'
		de_lang[_self.pwdNotEqual] = 'Passwörter sind nicht gleich.'
		de_lang[_self.nickIsTaken] = 'Nickname ist schon vergeben.'
		de_lang[_self.mailIsTaken] = 'E-Mail ist schon vergeben.'
		de_lang[_self.mailNotValid] = 'E-Mail ist nicht gültig.'
		de_lang[_self.mailSettingsTitle] = '(De-)Aktiviert Nachrichten in D-BAS.'
		de_lang[_self.notificationSettingsTitle] = '(De-)Aktiviert E-Mails von D-BAS.'
		de_lang[_self.errorTryLateOrContant] = 'Leider ist ein Fehler aufgetreten, bitte versuchen Sie später erneut oder kontaktieren Sie uns.'
		de_lang[_self.accountWasAdded] = 'Ihr Account wurde angelegt. Sie können sich nun anmelden.'
		de_lang[_self.accountRegistration] = 'D-BAS Beutzer Registrierung'
		de_lang[_self.accountWasRegistered] = 'Ihr Account wurde erfolgreich für die genannte E-Mail registiert.'
		de_lang[_self.accoutErrorTryLateOrContant] = 'Ihr Account konnte nicht angelegt werden, bitte versuchen Sie später erneut oder kontaktieren Sie uns.'
		de_lang[_self.nicknameIs] = 'Ihr Nickname lautet: '
		de_lang[_self.newPwdIs] = 'Ihr Passwort lautet: '
		de_lang[_self.dbasPwdRequest] = 'D-BAS Passwort Nachfrage'
		de_lang[_self.emailBodyText] = 'Dies ist eine automatisch generierte E-Mail von D-BAS.\nFür Kontakt können Sie gerne eine E-Mail an krauthoff@cs.uni-duesseldorf.de verfassen.\nDieses System ist Teil einer Promotion und noch in der Testphase.'
		de_lang[_self.emailWasSent] = 'E-Mail wurde gesendet.'
		de_lang[_self.emailWasNotSent] = 'E-Mail wurde nicht gesendet.'
		de_lang[_self.antispamquestion] = 'Was ist'
		de_lang[_self.signs] = ['+', '*', '/', '-']
		de_lang['0'] = 'null'
		de_lang['1'] = 'eins'
		de_lang['2'] = 'zwei'
		de_lang['3'] = 'drei'
		de_lang['4'] = 'vier'
		de_lang['5'] = 'fünf'
		de_lang['6'] = 'sechs'
		de_lang['7'] = 'sieben'
		de_lang['8'] = 'acht'
		de_lang['9'] = 'neun'
		de_lang['+'] = 'plus'
		de_lang['-'] = 'minus'
		de_lang['*'] = 'mal'
		de_lang['/'] = 'durch'
		de_lang[_self.defaultView] = 'Standardansicht'
		de_lang[_self.wideView] = 'Knoten trennen'
		de_lang[_self.tightView] = 'Kanten strecken'
		de_lang[_self.showContent] = 'Inhalt einblenden'
		de_lang[_self.hideContent] = 'Inhalt ausblenden'

		de_lang[_self.addATopic] = 'Thema hinzufügen'
		de_lang[_self.pleaseEnterTopic] = 'Bitte geben Sie Ihr Thema an:'
		de_lang[_self.pleaseEnterShorttextForTopic] = 'Bitte geben Sie die Kurzform Ihres Themas an:'
		de_lang[_self.pleaseSelectLanguageForTopic] = 'Bitte geben Sie die Sprache Ihres Themas an:'
		de_lang[_self.editStatementViewChangelog] = 'Aussagen editieren / Änderungprotokoll einsehen'
		de_lang[_self.editStatementHere] = 'Bitte bearbeiten Sie hier die Aussage:'
		de_lang[_self.save] = 'Sichern'
		de_lang[_self.cancel] = 'Abbrechen'
		de_lang[_self.submit] = 'Senden'
		de_lang[_self.close] = 'Schließen'
		de_lang[_self.urlSharing] = 'URL teilen'
		de_lang[_self.urlSharingDescription] = 'Teilen Sie diese URL:'
		de_lang[_self.warning] = 'Warnung'
		de_lang[_self.islandViewFor] = 'Inselansicht für'
		de_lang[_self.resumeHere] = 'Hier weitermachen'

		de_lang[_self.aand] = 'und'
		de_lang[_self.addStatementRow] = 'Fügt eine neue Reihe hinzu.'
		de_lang[_self.addedEverything] = 'Alles wurde hinzugefügt.'
		de_lang[_self.addTopic] = 'Thema hinzufügen'
		de_lang[_self.at] = 'am'
		de_lang[_self.alreadyInserted] = 'Dies ist ein Duplikat und schon vorhanden.'
		de_lang[_self.addPremisesRadioButtonText] = 'Lass\' mich meine eigenen Gründe angeben!'
		de_lang[_self.addArgumentsRadioButtonText] = 'Lass\' mich meine eigenen Aussagen angeben!'
		de_lang[_self.argumentContainerTextIfPremises] = 'Sie möchten Ihre eigenen Gründe angeben?'
		de_lang[_self.argumentContainerTextIfArguments] = 'Sie möchten Ihre eigenen Argumente angeben?'
		de_lang[_self.addPremiseRadioButtonText] = 'Lass\' mich meinen eigenen Grund angeben!'
		de_lang[_self.addArgumentRadioButtonText] = 'Lass\' mich meine eigene Aussage angeben!'
		de_lang[_self.argumentContainerTextIfPremise] = 'Sie möchten Ihren eigenen Grund angeben?'
		de_lang[_self.argumentContainerTextIfArgument] = 'Sie möchten Ihr eigenes Argument angeben?'
		de_lang[_self.argumentContainerTextIfConclusion] = 'Was ist Ihre Idee? Was sollten wir unternehmen?'
		de_lang[_self.argueAgainstPositionToggleButton] = 'Oder wenn Sie gegen eine Position argumentieren möchten, drücken Sie bitte diesen Schalter:'
		de_lang[_self.argueForPositionToggleButton] = 'Oder wenn Sie für eine Position argumentieren möchten, drücken Sie bitte diesen Schalter:'
		de_lang[_self.alternatively] = 'Alternativ'
		de_lang[_self.argument] = 'Argument'
		de_lang[_self.andIDoNotBelieveCounter] = 'und ich glaube, dass ist kein gutes Gegenargument für'
		de_lang[_self.andIDoNotBelieveArgument] = 'und ich glaube, dass ist kein gutes Argument für'
		de_lang[_self.andTheyDoNotBelieveCounter] = 'und sie glauben, dass ist kein gutes Gegenargument für'
		de_lang[_self.andTheyDoNotBelieveArgument] = 'und sie glauben, dass ist kein gutes Argument für'
		de_lang[_self.asReasonFor] = 'als einen Grund für'
		de_lang[_self.attackedBy] = 'Sie wurden attackiert mit'
		de_lang[_self.attackedWith] = 'Sie haben attackiert mit'
		de_lang[_self.attackPosition] = 'Position angreifen'
		de_lang[_self.agreeBecause] = 'Ich stimme zu, weil '
		de_lang[_self.andIDoBelieveCounterFor] = 'und ich glaube, dass ist ein gutes Gegenargument für'
		de_lang[_self.andIDoBelieveArgument] = 'und ich glaube, dass ist ein gutes Argument für'
		de_lang[_self.addArguments] = 'Argumente hizufügen'
		de_lang[_self.addStatements] = 'Aussagen hizufügen'
		de_lang[_self.addArgumentsTitle] = 'Fügt neue Argumente hinzu'
		de_lang[_self.acceptItTitle] = 'Einsenden...'
		de_lang[_self.acceptIt] = 'Eintragen...'
		de_lang[_self.attitudeFor] = 'Einstellungen zu'
		de_lang[_self.breadcrumbsStart] = 'Start'
		de_lang[_self.breadcrumbsChoose] = 'Mehrere Gründe für'
		de_lang[_self.breadcrumbsJustifyStatement] = 'Wieso denken Sie das'
		de_lang[_self.breadcrumbsGetPremisesForStatement] = 'Prämissen'
		de_lang[_self.breadcrumbsMoreAboutArgument] = 'Mehr Über'
		de_lang[_self.breadcrumbsReplyForPremisegroup] = 'Antwort für Gruppe'
		de_lang[_self.breadcrumbsReplyForResponseOfConfrontation] = 'Begründung von'  # Antwort für die Konfrontation'
		de_lang[_self.breadcrumbsReplyForArgument] = 'Antwort fürs Argument'
		de_lang[_self.butOtherParticipantsDontHaveOpinionRegardingYourOpinion] = 'aber andere Teilnehmer haben keine Meinung bezüglich ihrer Eingabe'
		de_lang[_self.butOtherParticipantsDontHaveArgument] = 'aber andere Teilnehmer haben keine Begründung für dafür'
		de_lang[_self.butOtherParticipantsDontHaveCounterArgument] = 'aber andere Teilnehmer haben kein Gegenargument.'
		de_lang[_self.butIDoNotBelieveCounterFor] = 'aber ich glaube nicht, dass es ein gutes Argument dagegen ist, dass'
		de_lang[_self.butIDoNotBelieveReasonForReject] = 'aber ich glaube nicht, dass das zur Aussage führt'
		de_lang[_self.butIDoNotBelieveArgumentFor] = 'aber ich glaube nicht, dass es ein gutes Argument dafür ist, dass'
		de_lang[_self.butTheyDoNotBelieveCounter] = 'aber sie glauben, dass es kein gutes Argument dagegen ist, dass' 
		de_lang[_self.butTheyDoNotBelieveArgument] = 'aber sie glauben, dass es kein gutes Argument dafür ist, dass' 
		de_lang[_self.butThenYouCounteredWith] = 'Jedoch haben Sie dann das Gegenargument gebracht, dass'
		de_lang[_self.butYouCounteredWith] = 'Jedoch haben Sie das Gegenargument gebracht, dass'
		de_lang[_self.butYouAgreedWith] = 'Und Sie haben zugestimmt, weil'
		de_lang[_self.because] = 'Weil'
		de_lang[_self.butWhich] = 'aber welches'
		de_lang[_self.clickHereForRegistration] = 'Klick <a href="" data-toggle="modal" data-target="#popup-login" title="Login">hier</a> für die Anmeldung oder eine Registrierung!'
		de_lang[_self.clickForMore] = 'Klick hier!'
		de_lang[_self.confirmation] = 'Bestätigung'
		de_lang[_self.contactSubmit] = 'Absenden der Nachricht'
		de_lang[_self.contact] = 'Kontakt'
		de_lang[_self.confirmTranslation] = 'Wenn Sie die Sprache ändern, geht Ihr aktueller Fortschritt verloren!'
		de_lang[_self.correctionsSet] = 'Ihre Korrektur wurde gesetzt.'
		de_lang[_self.countOfArguments] = 'Anzahl der Argumente'
		de_lang[_self.countOfPosts] = 'Anzahl der Beiträge'
		de_lang[_self.checkFirstname] = 'Bitte überprüfen Sie Ihren Vornamen, da die Eingabe leer ist!'
		de_lang[_self.checkLastname] = 'Bitte überprüfen Sie Ihren Nachnamen, da die Eingabe leer ist!'
		de_lang[_self.checkNickname] = 'Bitte überprüfen Sie Ihren Spitznamen, da die Eingabe leer ist!'
		de_lang[_self.checkEmail] = 'Bitte überprüfen Sie Ihre E-Mail, da die Eingabe leer ist!'
		de_lang[_self.checkPassword] = 'Bitte überprüfen Sie Ihre Passwort, da die Eingabe leer ist!'
		de_lang[_self.checkConfirmation] = 'Bitte überprüfen Sie Ihre Passwort-Bestätigung, da die Eingabe leer ist!'
		de_lang[_self.checkPasswordConfirm] = 'Bitte überprüfen Sie Ihre Passwörter, da die Passwärter nicht gleich sind!'
		de_lang[_self.clickToChoose] = 'Klicken zum wählen'
		de_lang[_self.clearStatistics] = 'Statistik löschen'
		de_lang[_self.canYouGiveAReason] = 'Können Sie einen Grund angeben?'
		de_lang[_self.canYouGiveAReasonFor] = 'Können Sie einen Grund für folgendes angeben:'
		de_lang[_self.canYouGiveACounterArgumentWhy1] = 'Können Sie begründen, wieso sie gegen'
		de_lang[_self.canYouGiveACounterArgumentWhy2] = 'sind?'
		de_lang[_self.canYouGiveACounter] = 'Können Sie einen Grund dagegen angeben?'
		de_lang[_self.canYouGiveAReasonForThat] = 'Können Sie dafür einen Grund angeben?'
		de_lang[_self.completeView] = 'Komplette View'
		de_lang[_self.completeViewTitle] = 'Kompletten Graphen anzeigen'
		de_lang[_self.currentDiscussion] = 'Die aktuelle Diskussion hat folgendes Thema'
		de_lang[_self.dialogView] = 'Dialog-Ansicht'
		de_lang[_self.dialogViewTitle] = 'Dialog-Ansicht'
		de_lang[_self.dateString] = 'Datum'
		de_lang[_self.disagreeBecause] = 'Ich widerspreche, weil '
		de_lang[_self.description_undermine] = 'Diese Aussage ist gegen die Prämisse.'
		de_lang[_self.description_support] = 'Diese Aussage ist für die Prämisse.'
		de_lang[_self.description_undercut] = 'Diese Aussage ist gegen die Begründung (undercut). Sie glauben nicht, dass aus der Prämisse die Konklusion folgt.'
		de_lang[_self.description_overbid] = 'Diese Aussage ist für die Begründung (overbid). Sie glauben nicht, dass aus der Prämisse die Konklusion folgt.'
		de_lang[_self.description_rebut] = 'Diese Aussage ist gegen die Konklusion.'
		de_lang[_self.description_no_opinion] = 'Sie haben keine Meinung odeWas ist Ihre Meinung?r möchten diesen Punkt nur überpringen.'
		de_lang[_self.decisionIndex7] = 'Entscheidungs Index - Letzte 7 Tage'
		de_lang[_self.decisionIndex30] = 'Entscheidungs Index - Letzte 30 Tage'
		de_lang[_self.decisionIndex7Info] = 'Anzahl an getroffenen Entscheidungen (bedingt durch Klicks im System), in den letzten 7 Tage'
		de_lang[_self.decisionIndex30Info] = 'Anzahl an getroffenen Entscheidungen (bedingt durch Klicks im System), in den letzten 30 Tage'
		de_lang[_self.dataRemoved] = 'Daten wurden erfolgreich gelöscht.'
		de_lang[_self.didYouMean] = 'Top 10 der Aussagen, die Sie eventuell meinten:'
		de_lang[_self.discussionEnd] = 'Die Diskussion endet hier.'
		de_lang[_self.discussionEndLinkText] = 'Sie können <a id="discussionEndStepBack" onclick="window.history.back();" style="cursor: pointer;">hier</a> klicken, um einen Schritt zurückzugehen oder den oberen Button bzw. <a href="" id="discussionEndRestart">diesen Link</a> nutzen, um die Diskussion neu zustarten.'
		de_lang[_self.duplicateDialog] = 'Diese Textversion ist veraltet, weil Sie schon editiert wurde.\nMöchten Sie diese Version dennoch als die aktuellste markieren?'
		de_lang[_self.duplicate] = 'Duplikat'
		de_lang[_self.displayControlDialogGuidedTitle] = 'geführte Ansicht'
		de_lang[_self.displayControlDialogGuidedBody] = 'Du wirst nie etwas wie eine Argumentationskarte sehen, da das System dich führt. Das System ist daher dynamisch und generisch für dich.'
		de_lang[_self.displayControlDialogIslandTitle] = 'Insel-Ansicht'
		de_lang[_self.displayControlDialogIslandBody] = 'Okay, Sie möchten mehr sehen, aber nicht alles? Genau dafür haben wie eine Insel-Ansicht als weitere Modus. Mit dieser Möglichkeit sehen Sie alle Aussagen, die mit Ihrem aktuellen Standpunkt verbunden sind.'
		de_lang[_self.displayControlDialogExpertTitle] = 'Experten-Ansicht'
		de_lang[_self.displayControlDialogExpertBody] = 'Du bist also ein Experte? Okay, dann darfst du wirklich alles auf einen Blick sehen.'
		de_lang[_self.discussionInfoTooltip1] = 'Die Diskussion wurde vor'
		de_lang[_self.discussionInfoTooltip2] = 'gestartet und hat schon'
		de_lang[_self.discussionInfoTooltip3pl] = 'Argument.'
		de_lang[_self.discussionInfoTooltip3sg] = 'Argumente.'
		de_lang[_self.doesNotHold] = 'ist keine gute Idee'
		de_lang[_self.doesNotHoldBecause] = 'ist nicht richtig, weil'
		de_lang[_self.doesJustify] = 'gerechtfertigen, dass'
		de_lang[_self.doesNotJustify] = 'nicht gerechtfertigen, dass'
		de_lang[_self.deleteTrack] = 'Track löschen'
		de_lang[_self.deleteHistory] = 'History löschen'
		de_lang[_self.doYouWantToEnterYourStatements] = 'Möchten Sie Ihre eigenen Gründe angeben?'
		de_lang[_self.doNotHesitateToContact] = 'Zögern Sie nicht, uns zu <span style="cursor: pointer;" id="contact-on-error"><strong>kontaktieren (hier klicken)</strong></span>'
		de_lang[_self.earlierYouArguedThat] = 'Zuerst haben Sie argumentiert, dass'
		de_lang[_self.editIndex] = 'Änderungs Index - Letzte 30 Tage'
		de_lang[_self.editIndexInfo] = 'Anzahl an Änderungen'
		de_lang[_self.euCookiePopupTitle] = 'Diese Seite nutzt Cookies und Piwik.'
		de_lang[_self.euCookiePopupText] = 'Wir benutzen Sie, um Ihnen die beste Erfahrung zu geben. Wenn Sie unsere Seite weiter nutzen, nehmen Sie alle Cookies unserer Seite an und sind glücklich damit. Zusätzlich tracken wir Ihre Aktionen und speichern diese anonym ab. Dabei wird Ihre IP-Adresse maskiert.'
		de_lang[_self.euCookiePopoupButton1] = 'Weiter'
		de_lang[_self.euCookiePopoupButton2] = 'Lerne&nbsp;mehr'
		de_lang[_self.empty_news_input] = 'Nachrichten-Titel oder Text ist leer oder zu kurz!'
		de_lang[_self.empty_notification_input] = 'Nachrichten-Titel oder Text ist leer oder zu kurz!'
		de_lang[_self.email] = 'E-Mail'
		de_lang[_self.emailWasSent] = 'Eine E-Mail wurde zu der genannten Adresse gesendet.'
		de_lang[_self.emailWasNotSent] = 'Ihre E-Mail konnte nicht gesendet werden!'
		de_lang[_self.emailUnknown] = 'Die Adresse ist nicht gültig.'
		de_lang[_self.edit] = 'Bearbeiten'
		de_lang[_self.error_code] = 'Fehler-Code'
		de_lang[_self.editTitle] = 'Aussagen bearbeiten'
		de_lang[_self.feelFreeToLogin] = 'Wenn Sie weiter machen möchten, <u><a href="" data-toggle="modal" data-target="#popup-login" title="Anmelden">melden</a></u> Sie sich bitte an :)'
		de_lang[_self.forText] = 'für'
		de_lang[_self.fillLine] = 'Bitte, füllen Sie diese Zeilen mit Ihrer Meldung'
		de_lang[_self.firstConclusionRadioButtonText] = 'Lass mich meine eigenen Ideen einfügen!'
		de_lang[_self.firstArgumentRadioButtonText] = 'Lass mich meine eigenen Aussagen einfügen!'
		de_lang[_self.feelFreeToShareUrl] = 'Bitte teilen Sie diese URL'
		de_lang[_self.fetchLongUrl] = 'Normale URL'
		de_lang[_self.fetchShortUrl] = 'Kurze URL'
		de_lang[_self.forgotPassword] = 'Passwort vergessen'
		de_lang[_self.firstOneText] = 'Sie sind der Erste, der sagt: '
		de_lang[_self.firstOneInformationText] = 'Sie sind der Erste, der Informationen haben möchte, über: '
		de_lang[_self.firstOneReason] = 'Sie sind der Erste mit diesem Argument. Bitte geben Sie Ihre Begründung an.'
		de_lang[_self.firstPositionText] = 'Sie sind der Erste in dieser Diskussion!'
		de_lang[_self.firstPremiseText1] = 'Sie sind der Erste, der sagt:'
		de_lang[_self.firstPremiseText2] = 'Bitte begründen Sie Ihre Aussage.'
		de_lang[_self.firstname] = 'Vorname'
		de_lang[_self.fromm] = 'von'
		de_lang[_self.finishTitle] = 'Diskussion beenden'
		de_lang[_self.hold] = 'stimmt'
		de_lang[_self.gender] = 'Geschlecht'
		de_lang[_self.goBack] = 'Zurück'
		de_lang[_self.goHome] = 'Startseite'
		de_lang[_self.goStepBack] = 'Einen Schritt zurück'
		de_lang[_self.generateSecurePassword] = 'Generate secure password'
		de_lang[_self.goodPointTakeMeBackButtonText] = 'Ich stimme zu, dass ist ein gutes Argument. Geh einen Schritt zurück.'
		de_lang[_self.group_uid] = 'Gruppe'
		de_lang[_self.haveALookAt] = 'Hey, schau dir mal das an: '
		de_lang[_self.hidePasswordRequest] = 'Verstecke die Passwort-Anfrage'
		de_lang[_self.hideGenerator] = 'Verstecke Generator'
		de_lang[_self.history] = 'Geschichte'
		de_lang[_self.howeverIHaveMuchStrongerArgumentRejecting] = 'Jedoch habe ich ein viel stärkeres Argument dagegen, dass'
		de_lang[_self.howeverIHaveEvenStrongerArgumentRejecting] = 'Jedoch habe ich ein stärkeres Argument gegen:'
		de_lang[_self.howeverIHaveMuchStrongerArgumentAccepting] = 'Jedoch habe ich ein viel stärkeres Argument dafür, dass'
		de_lang[_self.howeverIHaveEvenStrongerArgumentAccepting] = 'Jedoch habe ich ein stärkeres Argument für:'
		de_lang[_self.internalFailureWhileDeletingTrack] = 'Interner Fehler, bitte versuchen Sie es später erneut.'
		de_lang[_self.internalFailureWhileDeletingHistory] = 'Interner Fehler, bitte versuchen Sie es später erneut.'
		de_lang[_self.internalError] = '<strong>Interner Fehler:</strong> Wahrscheinlich ist der Server nicht erreichbar. Bitte laden Sie die Seite erneut!.'
		de_lang[_self.inputEmpty] = 'Ihre Eingabe ist leer!'
		de_lang[_self.informationForExperts] = 'Infos für Experten'
		de_lang[_self.issueList] = 'Themen'
		de_lang[_self.islandViewHeaderText] = 'Dies sind alle Argumente für: '
		de_lang[_self.irrelevant] = 'Irrelevant'
		de_lang[_self.itIsTrue] = 'sie akzeptieren, dass'
		de_lang[_self.itIsFalse] = 'sie lehnen ab, dass'
		de_lang[_self.itTrueIs] = 'es richtig ist, dass'
		de_lang[_self.itFalseIs] = 'es falsch ist, dass'
		de_lang[_self.islandView] = 'Insel Ansicht'
		de_lang[_self.isFalse] = 'ist falsch'
		de_lang[_self.isTrue] = 'richtig ist'
		de_lang[_self.isNotAGoodIdea] = 'falsch ist'
		de_lang[_self.initialPosition] = 'Anfangs-interesse'
		de_lang[_self.initialPositionSupport] = 'Was ist Ihre Meinung, die Sie unterstützen?'
		de_lang[_self.initialPositionAttack] = 'Was ist Ihre Meinung, di Sie angreifen möchten?'
		de_lang[_self.initialPositionInterest] = 'Ich möchte über die Aussage reden, dass ...'
		de_lang[_self.islandViewTitle] = 'Zeigt die Insel Ansicht'
		de_lang[_self.iAcceptCounter] = 'und ich akzeptiere, dass es ein Argument dagegen ist, dass' 
		de_lang[_self.iAcceptArgument] = 'und ich akzeptiere, dass es ein Argument dafür ist, dass' 
		de_lang[_self.iAgreeWith] = 'Ich akzeptiere die Aussage, dass'
		de_lang[_self.iAgreeWithInColor] = 'Ich <span class=\'text-success\'>akzeptiere</span> die Aussage, dass'
		de_lang[_self.iDisagreeWith] = 'Ich widerspreche der Aussage, dass'
		de_lang[_self.iDisagreeWithInColor] = 'Ich <span class=\'text-danger\'>widerspreche</span> der Aussage, dass'
		de_lang[_self.iDoNotKnow] = 'Ich weiß es nicht, dass'
		de_lang[_self.iDoNotKnowInColor] = 'Ich <span class=\'text-info\'>weiß es nicht</span>, dass'
		de_lang[_self.iHaveNoOpinionYet] = 'Ich weiß es nicht, dass'
		de_lang[_self.iHaveNoOpinion] = 'Ich weiß es nicht'
		de_lang[_self.iHaveNoOpinionYetInColor] = 'Ich <span class=\'text-info\'>weiß es nicht</span>. Zeige mir eine Aussage dafür, dass'
		de_lang[_self.iHaveMuchStrongerArgumentRejecting] = 'Ich habe ein viel stärkeres Argument zum Ablehnen von'
		de_lang[_self.iHaveEvenStrongerArgumentRejecting] = 'Ich habe ein stärkeres Argument zum Ablehnen von'
		de_lang[_self.iHaveMuchStrongerArgumentAccepting] = 'Ich habe ein viel stärkeres Argument zum Akzeptieren von'
		de_lang[_self.iHaveEvenStrongerArgumentAccepting] = 'Ich habe ein stärkeres Argument zum Akzeptieren von'
		de_lang[_self.iNoOpinion] = 'Ich habe keine Meinung bezüglich'
		de_lang[_self.interestingOnDBAS] = 'Interessante Diskussion in D-BAS'
		de_lang[_self.informationForStatements] = 'Informationen zu den Aussagen'
		de_lang[_self.keyword] = 'Schlüsselwort'
		de_lang[_self.keywordStart] = 'Start'
		de_lang[_self.keywordChooseActionForStatement] = 'Einstellung zu'
		de_lang[_self.keywordGetPremisesForStatement] = 'Prämissen von'
		de_lang[_self.keywordMoreAboutArgument] = 'Mehr über'
		de_lang[_self.keywordReplyForPremisegroup] = 'Antwort auf das Argument'
		de_lang[_self.keywordReplyForResponseOfConfrontation] = 'Begründung von'
		de_lang[_self.keywordReplyForArgument] = 'Konfrontation'
		de_lang[_self.keepSetting] = 'Entscheidung merken'
		de_lang[_self.holds] = 'ist richtig'
		de_lang[_self.hideAllUsers] = 'Verstecke alle Benutzer'
		de_lang[_self.hideAllAttacks] = 'Verstecke alle Angriffe'
		de_lang[_self.letMeExplain] = 'Lass\' es mich so erklären'
		de_lang[_self.levenshteinDistance] = 'Levenshtein-Distanz'
		de_lang[_self.languageCouldNotBeSwitched] = 'Leider konnte die Sprache nicht gewechselt werden'
		de_lang[_self.last_action] = 'Letzte Aktion'
		de_lang[_self.last_login] = 'Letze Anmeldung'
		de_lang[_self.login] = 'Login'
		de_lang[_self.logfile] = 'Logdatei für'
		de_lang[_self.letsGo] = 'Klicken Sie hier um direkt zu starten!'
		de_lang[_self.letsGoBack] = 'Ab geht\'s zurück!'
		de_lang[_self.letsGoHome] = 'Ab zur Startseite!'
		de_lang[_self.more] = 'Mehr'
		de_lang[_self.medium] = 'mittel'
		de_lang[_self.newPremisesRadioButtonText] = 'Nichts von all dem. Ich habe neue Gründe!'
		de_lang[_self.newPremisesRadioButtonTextAsFirstOne] = 'Ja, ich möchte neue Gründe angeben!'
		de_lang[_self.newStatementsRadioButtonTextAsFirstOne] = 'Ja, ich möchte neue Aussagen angeben!'
		de_lang[_self.newPremiseRadioButtonText] = 'Nichts von all dem. Ich möchte einen neuen Grund angeben!'
		de_lang[_self.newPremiseRadioButtonTextAsFirstOne] = 'Ja, ich möchte einen neuen Grunde angeben!'
		de_lang[_self.newStatementRadioButtonTextAsFirstOne] = 'Ja, ich möchte eine neue Aussage angeben!'
		de_lang[_self.newConclusionRadioButtonText] = 'Nichts von all dem. Ich habe eine andere Idee!'
		de_lang[_self.newsAboutDbas] = 'Nachrichten über D-BAS'
		de_lang[_self.next] = 'Nächster Eintrag'
		de_lang[_self.nickname] = 'Spitzname'
		de_lang[_self.noOtherAttack] = 'Das System hat kein weiteres Gegenargument'
		de_lang[_self.noIslandView] = 'Daten für die Island View konnten nicht geladen werden. Tschuldigung!'
		de_lang[_self.noCorrections] = 'Keinte Korreturen für die aktuelle Aussage.'
		de_lang[_self.noDecisionDone] = 'Es liegt keine Entscheidung vor.'
		de_lang[_self.noCorrectionsSet] = 'Korrektur wurde nicht gespeichert, da der Benutzer unbekannt ist. Sind Sie angemeldet?'
		de_lang[_self.notInsertedErrorBecauseEmpty] = 'Ihre Idee wurde nicht gespeichert, da das Feld leer oder der Inhalt zu kurz ist.'
		de_lang[_self.notInsertedErrorBecauseDuplicate] = 'Ihre Idee wurde nicht gespeichert, da Ihre Idee ein Duplikat ist.'
		de_lang[_self.notInsertedErrorBecauseUnknown] = 'Ihre Idee wurde aufgrund eines unbekannten Fehlers nicht gespeichert.'
		de_lang[_self.notInsertedErrorBecauseInternal] = 'Ihre Idee wurde aufgrund eines internen Fehlers nicht gespeichert.'
		de_lang[_self.noEntries] = 'Keine Einträge vorhanden'
		de_lang[_self.noTrackedData] = 'Keine Daten wurden gespeichert.'
		de_lang[_self.number] = 'Nr'
		de_lang[_self.note] = 'Hinweis'
		de_lang[_self.now] = 'Jetzt'
		de_lang[_self.no_entry] = 'Kein Eintrag'
		de_lang[_self.noRights] = 'Sie haben nicht genügend Rechte!'
		de_lang[_self.notLoggedIn] = 'Sie sind nicht angemeldet!'
		de_lang[_self.on] = 'An'
		de_lang[_self.off] = 'Aus'
		de_lang[_self.onlyOneItem] = 'Sofern Sie eine neue Aussage hinzufügen möchten, klicken Sie bitte hier um sich anzumelden.'
		de_lang[_self.onlyOneItemWithLink] = 'Sofern Sie eine neue Aussage hinzufügen möchten, klicken Sie bitte <a href="" data-toggle="modal" data-target="#popup-login" title="Login">hier</a> um sich anzumelden.'
		de_lang[_self.unfortunatelyOnlyOneItem] = 'Leider gibt es nur eine Auswahl. Sofern Sie eine neue Aussage hinzufügen möchten, klicken Sie bitte <a href="" data-toggle="modal" data-target="#popup-login" title="Login">hier</a> m sich anzumelden.'
		de_lang[_self.otherParticipantsConvincedYouThat] = 'Andere Teilnehmer haben Sie überzeuge, dass'
		de_lang[_self.otherParticipantsThinkThat] = 'Andere Teilnehmer denken, dass'
		de_lang[_self.otherParticipantsAgreeThat] = 'Andere Teilnehmer stimmen zu, dass'
		de_lang[_self.otherParticipantsDontHaveOpinion] = 'Andere Teilnehmer haben keine Meinung, dazu dass'
		de_lang[_self.otherParticipantsDontHaveOpinionRegaringYourSelection] = 'Andere Teilnehmer haben keine Meinung zu Ihrer Aussage'
		de_lang[_self.otherParticipantsDontHaveCounter] = 'Andere Teilnehmer haben kein Gegenargument für '
		de_lang[_self.otherParticipantsDontHaveCounterForThat] = 'Andere Teilnehmer haben kein Gegenargument dafür'
		de_lang[_self.otherParticipantsDontHaveNewCounterForThat] = 'Andere Teilnehmer haben kein neues Gegenargument dafür. Sie habe schon alle Gegenargumente gesehen.'
		de_lang[_self.otherParticipantsDontHaveArgument] = 'Andere Teilnehmer haben kein Argument für '
		de_lang[_self.otherParticipantsAcceptBut] = 'Andere Teilnehmer akzeptieren Ihr Argument, aber'
		de_lang[_self.otherParticipantDisagreeThat] = 'Andere Teilnehmer widersprechen, dass '
		de_lang[_self.otherUsersClaimStrongerArgumentRejecting] = 'Andere Teilnehmer haben eine stärkere Aussage zur Ablehnung davon dass,'
		de_lang[_self.otherUsersClaimStrongerArgumentAccepting] = 'Andere Teilnehmer haben eine stärkere Aussage zur Annahme davon dass,'
		de_lang[_self.otherUsersHaveCounterArgument] = 'Andere Teilnehmer haben das Gegenargument, dass'
		de_lang[_self.otherUsersSaidThat] = 'Andere Teilnehmer haben gesagt, dass'
		de_lang[_self.opinionBarometer] = 'Meinungsbarometer'
		de_lang[_self.pleaseAddYourSuggestion] = 'Bitte geben Sie Ihren Vorschlag an!'
		de_lang[_self.previous] = 'Vorheriger Eintrag'
		de_lang[_self.premiseGroup] = 'Gruppe von Voraussetzung(en)'
		de_lang[_self.publicNickTitle] = '(De-)Aktiviert Ihren richtigen Nickname auf Ihrer öffentlichen Seite'
		de_lang[_self.passwordSubmit] = 'Passwort ändern'
		de_lang[_self.report] = 'Melden'
		de_lang[_self.reportTitle] = 'Verstoß melden'
		de_lang[_self.remStatementRow] = 'Entfernt diese Reihe.'
		de_lang[_self.registered] = 'Registriert'
		de_lang[_self.right] = 'Ja'
		de_lang[_self.requestTrack] = 'Track anfragen'
		de_lang[_self.refreshTrack] = 'Track neuladen'
		de_lang[_self.requestHistory] = 'History anfragen'
		de_lang[_self.refreshHistory] = 'History neuladen'
		de_lang[_self.requestFailed] = 'Anfrage fehlgeschlagen'
		de_lang[_self.restartDiscussion] = 'Diskussion neustarten'
		de_lang[_self.restartDiscussionTitle] = 'Diskussion neustarten'
		de_lang[_self.restartOnError] = 'Bitte laden Sie die Seite erneut oder starten Sie die Diskussion neu, sofern der Fehler bleibt.'
		de_lang[_self.recipientNotFound] = 'Empfänger konnte nicht gefunden werden.'
		de_lang[_self.reactionFor] = 'Reaktionen zu'
		de_lang[_self.questionTitle] = 'Erhalten Sie mehr Informationen über die Aussage!'
		de_lang[_self.saveMyStatement] = 'Aussage speichern!'
		de_lang[_self.selectStatement] = 'Bitte Wählen Sie eine Aussage!'
		de_lang[_self.showAllUsers] = 'Zeig\' alle Benutzer'
		de_lang[_self.showAllArguments] = 'Zeig\' alle Argumente'
		de_lang[_self.showAllArgumentsTitle] = 'Zeigt alle Argumente'
		de_lang[_self.showAllUsersTitle] = 'Zeige alle Nutzer'
		de_lang[_self.strength] = 'Stärke'
		de_lang[_self.strong] = 'stark'
		de_lang[_self.strongerStatementForAccepting] = 'aber Sie haben eine stärkere Aussage zur Annahme, davon dass'
		de_lang[_self.strongerStatementForRecjecting] = 'aber Sie haben eine stärkere Aussage zur Ablehnung, davon dass'
		de_lang[_self.soYouEnteredMultipleReasons] = 'Sie haben mehrere Gründe eingegeben'
		de_lang[_self.soYourOpinionIsThat] = 'Ihre Meinung ist, dass'
		de_lang[_self.soYouWantToArgueAgainst] = 'Sie möchten ein Gegenargument bringen für'
		de_lang[_self.soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion] = 'sodass andere Teilnehmer haben keine Meinung bezüglich ihrer Eingabe'
		de_lang[_self.shortenedBy] = 'welche gekürzt wurde mit'
		de_lang[_self.shareUrl] = 'Link teilen'
		de_lang[_self.showMeAnotherArgument] = 'Zeige mir ein weiteres Argument'
		de_lang[_self.switchDiscussion] = 'Diskussionsthema ändern'
		de_lang[_self.switchDiscussionTitle] = 'Diskussionsthema ändern'
		de_lang[_self.switchDiscussionText1] = 'Wenn Sie akzeptieren, wird das Diskussionsthema gewechselt zu'
		de_lang[_self.switchDiscussionText2] = 'und die Diskussion neugestartet.'
		de_lang[_self.switchLanguage] = 'Sprache ändern'
		de_lang[_self.supportPosition] = 'Position unterstützen'
		de_lang[_self.statement] = 'Aussage'
		de_lang[_self.statementIndex] = 'Aussagen Index - Letzte 30 Tage'
		de_lang[_self.statementIndexInfo] = 'Anzahl an hinzugefügten Aussagen'
		de_lang[_self.sureThat] = 'Ich bin sehr sicher, dass '
		de_lang[_self.surname] = 'Nachname'
		de_lang[_self.showMeAnArgumentFor] = 'Zeig\' mir ein Argument für'
		de_lang[_self.textAreaReasonHintText] = 'Bitte nutzen Sie ein Feld für jeden Grund. Schreiben Sie kurz und prägnant!'
		de_lang[_self.theCounterArgument] = 'dem Gegenargument'
		de_lang[_self.therefore] = 'Daher'
		de_lang[_self.thinkWeShould] = 'Ich denke, wir sollten '
		de_lang[_self.thisConfrontationIs] = 'Dieser Angriff ist ein'
		de_lang[_self.track] = 'Spur'
		de_lang[_self.textversionChangedTopic] = 'Aussage wurde geändert'
		de_lang[_self.textversionChangedContent] = 'Ihr Text wurde geändert von'
		de_lang[_self.to] = 'zu'
		de_lang[_self.topicString] = 'Thema'
		de_lang[_self.text] = 'Text'
		de_lang[_self.theySay] = 'Sie sagen, dass'
		de_lang[_self.theyThink] = 'Sie denken, dass'
		de_lang[_self.thisIsACopyOfMail] = 'Dies ist eine Kopie Ihrer Mail'
		de_lang[_self.veryweak] = 'sehr schwach'
		de_lang[_self.wantToStateNewPosition] = 'Um eine neue Aussage hinzuzufügen, klicken Sie bitte hier um sich anzumelden.'
		de_lang[_self.weak] = 'schwach'
		de_lang[_self.wrong] = 'Nein'
		de_lang[_self.wouldYourShareArgument] = 'Können Sie einen Grund angeben?'
		de_lang[_self.wrongURL] = 'Ihre URL scheint falsch zu sein.'
		de_lang[_self.whatDoYouThinkAbout] = 'Was halten Sie davon, dass '
		de_lang[_self.whatDoYouThinkAboutThat] = 'Was denken Sie darüber'
		de_lang[_self.whatIsYourIdea] = 'Ich denke / meine, dass ...'
		de_lang[_self.whatIsYourMostImportantReasonFor] = 'Was ist Ihr wichtigster Grund für die Aussage'
		de_lang[_self.whatIsYourMostImportantReasonWhy] = 'Was ist Ihr wichtigster Grund dafür, dass '
		de_lang[_self.whyDoYouThinkThat] = 'Wieso denken Sie, dass'
		de_lang[_self.whyAreYouDisagreeingWith] = 'Warum sind sie dagegenen, dass'
		de_lang[_self.whyAreYouAgreeingWith] = 'Warum sind sie dafür, dass'
		de_lang[_self.whyAreYouDisagreeingWithInColor] = 'Warum sind sie <span class=\'text-danger\'>dagegenen</span>, dass'
		de_lang[_self.whyAreYouAgreeingWithInColor] = 'Warum sind sie <span class=\'text-success\'>dafür</span>, dass'
		de_lang[_self.whyAreYouDisagreeingWithThat] = 'Warum sind Sie anderer Meinung?'
		de_lang[_self.youMadeA] = 'Sie machten ein/e'
		de_lang[_self.youMadeAn] = 'Sie machten ein/e'
		de_lang[_self.relation_undermine] = 'ist ein Gegenargument für'
		de_lang[_self.relation_support] = 'ist ein Argument für'
		de_lang[_self.relation_undercut] = 'ist ein Gegenargument für'
		de_lang[_self.relation_overbid] = 'ist ein Argument für'
		de_lang[_self.relation_rebut] = 'ist ein Gegenargument für'
		de_lang[_self.uid] = 'ID'
		de_lang[_self.unfortunatelyNoMoreArgument] = 'Leider gibt es keine weiteren Argumente für'
		de_lang[_self.userPasswordNotMatch] = 'Benutzername und/oder Passwort stimmen nicht überein'
		de_lang[_self.userOptions] = 'Benutzeroptionen'
		de_lang[_self.voteCountTextFirst] = 'Sie sind der Erste mit dieser Meinung'
		de_lang[_self.voteCountTextMayBeFirst] = 'Sie wären der Erste mit dieser Meinung'
		de_lang[_self.voteCountTextOneOther] = 'Ein/e Andere/r mit dieser Meinung'
		de_lang[_self.voteCountTextMore] = 'weitere Teilnehmer/innen mit dieser Meinung'
		de_lang[_self.welcome] = 'Willkommen'
		de_lang[_self.welcomeMessage] = 'Willkommen im neuen Dialog-basierten Argumentations-System.<br>Wir wünschen viel Spaß beim Diskutieren!'
		de_lang[_self.youAreInterestedIn] = 'Sie interessieren Sich für'
		de_lang[_self.youAgreeWith] = 'Sie sind der Meinung, dass'
		de_lang[_self.youDisagreeWith] = 'Sie wiedersprechen, dass'
		de_lang[_self.youSaidThat] = 'Sie haben gesagt, dass'
		de_lang[_self.youUsedThisEarlier] = 'Sie haben diese Aussage schon benutzt.'
		de_lang[_self.youRejectedThisEarlier] = 'Sie haben diese Aussage schon abgelehnt.'
		de_lang[_self.youHaveMuchStrongerArgumentForAccepting] = 'Sie haben eine viel stärker Begründung für'
		de_lang[_self.youHaveMuchStrongerArgumentForRejecting] = 'Sie haben eine viel stärker Ablehnung für'

		return de_lang
