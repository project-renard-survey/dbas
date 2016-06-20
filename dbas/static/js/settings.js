/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function HistoryHandler(){
	'use strict';

	/**
	 * Ajax request for getting the users history
	 */
	this.getUserHistoryData = function(){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_history',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().getUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 * Ajax request for deleting the users history
	 */
	this.deleteUserHistoryData = function(){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_user_history',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().removeUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 *
	 * @param data
	 */
	this.getUserHistoryDataDone = function(data){
		new HistoryHandler().setDataInHistoryTable(data);
	};

	/**
	 *
	 * @param statuscode
	 */
	this.getDataFail = function(statuscode){
		$('#' + historyTableSuccessId).hide();
		$('#' + historyTableFailureId).fadeIn('slow');
		new Helper().delay(function() { $('#' + historyTableFailureId).fadeOut(); }, 3000);

		if (statuscode == 400) {		$('#' + historyFailureMessageId).html(_t(requestFailedBadToken));
		} else if (statuscode == 500) {	$('#' + historyFailureMessageId).html(_t(requestFailedInternalError));
		} else {                		$('#' + historyFailureMessageId).html(_t(requestFailed));
		}
	};

	/**
	 *
	 */
	this.removeUserHistoryDataDone = function(){
		$('#' + historyTableSpaceId).empty();
		$('#' + deleteHistoryButtonId).hide();
		$('#' + requestHistoryButtonId).hide();
		$('#' + historyTableSuccessId).show();
		$('#' + historyTableFailureId).hide();
		$('#' + historySuccessMessageId).text(_t(dataRemoved));
	};

	/**
	 *
	 * @param jsonData
	 */
	this.setDataInHistoryTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tElement, i, parsedData, thead, tbody, breaked_url, helper = new Helper();
		tElement = ['', ''];
		tableElement = $('<table>');
		tableElement
			.attr('class', 'table table-striped table-hover')
			.attr('border', '0')
			.attr('style', 'border-collapse: separate; border-spacing: 0px;');

		trElement = $('<tr>');
		thead = $('<thead>');
		tbody = $('<tbody>');

		for (i = 0; i < tElement.length; i += 1) {
			tElement[i] = $('<th>');
		}

		// add header row
		tElement[0] = $('<th>').text('#');
		tElement[1] = $('<th>').text('URL');
		tElement[2] = $('<th>').text(_t(timestamp));

		for (i = 0; i < tElement.length; i += 1) {
			trElement.append(tElement[i]);
		}
		thead.append(trElement);
		tableElement.append(thead);

		// adding the historys
		var has_data = false;
		parsedData = $.parseJSON(jsonData);
		$.each(parsedData, function setDataInHistoryTableEach(index, history) {
			has_data = true;
			breaked_url = helper.cutTextOnChar(history.path, 120, '/');
			tElement[0] = $('<td>').text(index);
			tElement[1] = $('<td>').html('<a href="' + history.path + '">' + history.path + '</a>');
			tElement[2] = $('<td>').text(history.timestamp);

			trElement = $('<tr>');
			for (i = 0; i < tElement.length; i += 1) {
				trElement.append(tElement[i]);
			}
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		if (has_data) {
			$('#' + historyTableSpaceId).empty().append(tableElement);
			$('#' + deleteHistoryButtonId).fadeIn('slow');
		} else {
			$('#' + historyTableSpaceId).empty();
			$('#' + historyTableSuccessId).show();
			$('#' + historySuccessMessageId).text(_t(noTrackedData));
			$('#' + deleteHistoryButtonId).hide();
			$('#' + requestHistoryButtonId).hide();
		}
	};

}

function PasswordHandler(){
	// check password strength
	// based on http://git.aaronlumsden.com/strength.js/
	var upperCase = new RegExp('[A-Z]'),
		lowerCase = new RegExp('[a-z]'),
		numbers = new RegExp('[0-9]'),
		keylist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!%&@#$?_~<>+-*/',
		specialchars = new RegExp('([!,%,&,@,#,$,^,*,?,_,~])');

	this.set_total = function (total, passwordMeter, passwordStrength, passwordExtras) {
		'use strict';
		passwordMeter.removeClass().addClass('col-sm-9');
		passwordStrength.text(_t(strength) + ': ' + _t(veryweak)).fadeIn("slow");

		if (total === 1) {			passwordMeter.addClass('veryweak');	passwordStrength.text(_t(strength) + ': ' + _t(veryweak));
		} else if (total === 2) {	passwordMeter.addClass('weak');		passwordStrength.text(_t(strength) + ': ' + _t(weak));
		} else if (total === 3) {	passwordMeter.addClass('medium');	passwordStrength.text(_t(strength) + ': ' + _t(medium));
		} else if (total > 3) {		passwordMeter.addClass('strong');	passwordStrength.text(_t(strength) + ': ' + _t(strong));
		} else if (passwordExtras){	passwordExtras.fadeOut('slow');
		}
	};

	/**
	 *
	 * @param passwordInput
	 * @param passwordMeter
	 * @param passwordStrength
	 * @param passwordExtras
	 */
	this.check_strength = function (passwordInput, passwordMeter, passwordStrength, passwordExtras) {
		'use strict';
		var total = 0,
			pw = passwordInput.val();
		if (pw.length > 8) {			total = total + 1;	}
		if (upperCase.test(pw)) {		total = total + 1;	}
		if (lowerCase.test(pw)) {		total = total + 1;	}
		if (numbers.test(pw)) {			total = total + 1;	}
		if (specialchars.test(pw)) {	total = total + 1;	}
		new PasswordHandler().set_total(total, passwordMeter, passwordStrength, passwordExtras);
	};

	/**
	 *
	 * @param output
	 */
	this.generate_password = function (output) {
		'use strict';
		var password = '',
			i = 0;
		while (!(upperCase.test(password) && lowerCase.test(password) && numbers.test(password) && specialchars.test(password))) {
			i = 0;
			password = '';
			for (i; i < 8; i = i + 1) {
				password += keylist.charAt(Math.floor(Math.random() * keylist.length));
			}
		}
		output.val(password);
		output.text(password);
	};
}

function SettingsHandler(){

	/**
	 *
	 * @param toggle_element
	 * @param service
	 */
	this.setUserSetting = function(toggle_element, service) {
		var settings_value = toggle_element.prop('checked');
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_setting',
			method: 'GET',
			data:{'settings_value': settings_value ? 'True': 'False', 'service': service},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function setUserSettingDone(data) {
			new SettingsHandler().callbackDone(data, toggle_element, settings_value, service);
		}).fail(function setUserSettingFail() {
			new SettingsHandler().callbackFail(toggle_element, settings_value, service);
		});
	};

	/**
	 *
	 * @param jsonData
	 * @param toggle_element
	 * @param settings_value
	 * @param service
	 */
	this.callbackDone = function (jsonData, toggle_element, settings_value, service){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length == 0){
			$('#' + settingsSuccessDialog).fadeIn();
			$('#value_public_nickname').text(parsedData.public_nick);
			$('#value_public_page').attr('href', parsedData.public_page_url);
			new Helper().delay(function() { $('#' + settingsSuccessDialog).fadeOut(); }, 3000);
		} else {
			new SettingsHandler().callbackReceiveFail(toggle_element, settings_value, service);
		}
	};

	/**
	 *
	 * @param toggle_element
	 * @param settings_value
	 * @param service
	 */
	this.callbackFail = function (toggle_element, settings_value, service){
		$('#' + settingsAlertDialog).fadeIn();
		new Helper().delay(function() { $('#' + settingsAlertDialog).fadeOut(); }, 3000);
		toggle_element.off('change').bootstrapToggle(settings_value ? 'off' : 'on').change(function() {
			new SettingsHandler().setUserSetting(toggle_element, service);
		});
	}

}

function StatisticsHandler(){

	/**
	 *
	 */
	this.getEditsDone = function() {
		if ($('#' + editsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_edits',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allEditsDone), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 *
	 */
	this.getStatementsSend = function() {
		if ($('#' + statementsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_posted_statements',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 *
	 */
	this.getArgumentVotes = function(){
		if ($('#' + discussionArgVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_argument_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 *
	 */
	this.getStatementVotes = function(){
		if ($('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_statement_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 *
	 */
	this.deleteStatistics = function(){
		if ($('#' + editsDoneCountId).text() == '0' &&
			$('#' + discussionArgVoteCountId).text() == '0' &&
			$('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}
		// display dialog
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' h4.modal-title').text(_t(deleteStatisticsTitle));
		$('#' + popupConfirmDialogId + ' div.modal-body').html(_t(deleteStatisticsBody));
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
			new StatisticsHandler().deleteStatisticsRequest()
		});
		$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		});
	};

	/**
	 *
	 */
	this.deleteStatisticsRequest = function() {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_statistics',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackDeleteStatisticsDone(data);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail();
		});
	};

	/**
	 *
	 * @param jsonData
	 * @param titleText
	 * @param is_vote
	 */
	this.callbackGetStatisticsDone = function(jsonData, titleText, is_vote){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.length == 0){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var table, tr, span_up, span_down, modalBody;
		table = $('<table>');
		table.attr('class', 'table table-condensed table-hover')
			.attr('border', '0')
			.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
		tr = $('<tr>')
			.append($('<td>').html('<strong>' + _t(text) + '</strong>').css('text-align', 'center'))
			.append($('<td>').html('<strong>' + _t(date) + '</strong>').css('text-align', 'center'));
		if (is_vote) {
			tr.append($('<td>').html('<strong>' + _t(typeofVote) + '</strong>').css('text-align', 'center'))
				.append($('<td>').html('<strong>' + _t(valid) + '</strong>').css('text-align', 'center'));
		}
		table.append(tr);

		span_up = $('<span>').addClass('glyphicon').addClass('glyphicon glyphicon-thumbs-up').attr('aria-hidden', 'true');
		span_down = $('<span>').addClass('glyphicon').addClass('glyphicon glyphicon-thumbs-down').attr('aria-hidden', 'true');

		$.each(parsedData, function callbackGetStatisticsDoneTableEach(key, val) {
			tr = $('<tr>')
				.append($('<td>').text(val.timestamp))
				.append($('<td>').text(is_vote ? val.text : val.content));
			if (is_vote) {
				tr.append($('<td>').html(val.is_up_vote ? span_up.clone() : span_down.clone()).css('text-align', 'center'))
					.append($('<td>').html(val.is_valid ? checkmark : ballot).css('text-align', 'center'));
			}
			table.append(tr);
		});

		$('#' + popupConfirmDialogId).off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
			// re-hanging our modal body and delete the slimscrolldiv
			var modalbody = $('.slimScrollDiv').children().eq(0);
			modalbody.children().eq(1).remove();
			modalbody.children().eq(2).remove();
			$('.modal-header').after(modalbody);
			$('.slimScrollDiv').remove();
		}).modal('show').find('.modal-dialog').addClass('modal-lg');

		$('#' + popupConfirmDialogId + ' h4.modal-title').text(titleText);
		modalBody = $('#' + popupConfirmDialogId + ' div.modal-body');
		modalBody.empty().append(table);

		$('#' + popupConfirmDialogAcceptBtn).hide();
		$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
			$(".scrollarea").slimScroll({destroy:true});
		}).removeClass('btn-danger').text('Okay');

		new Helper().delay(function() {
			if (modalBody.height() > (window.innerHeight-250)){
				modalBody.slimScroll({
					position: 'right',
					height: (window.innerHeight-250) + 'px',
					railVisible: true,
					alwaysVisible: false
				});
			} else {
				$(".scrollarea").slimScroll({destroy:true});
			}
		}, 250);
	};

	/**
	 *
	 * @param jsonData
	 */
	this.callbackDeleteStatisticsDone = function(jsonData) {
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.removed_data == 'true') {
			$('#' + statisticsSuccessDialog).fadeIn();
			$('#' + statisticsSuccessMessage).text(_t(statisticsDeleted));
			new Helper().delay(function () {
				$('#' + statisticsSuccessDialog).fadeOut();
			}, 3000);
			$('#' + editsDoneCountId).text('0');
			$('#' + discussionArgVoteCountId).text('0');
			$('#' + discussionStatVoteCountId).text('0');
		} else {
			new StatisticsHandler().callbackStatisticsFail();
		}
	};

	/**
	 *
	 * @param text
	 */
	this.callbackStatisticsFail = function(text){
		$('#' + statisticsAlertDialog).fadeIn();
		$('#' + statisticsAlertMessage).text(text);
		new Helper().delay(function() { $('#' + statisticsAlertDialog).fadeOut(); }, 3000);
	};

}

$(function () {
	'use strict';
	var settingsPasswordExtras = $('#' + settingsPasswordExtrasId);

	$('#' + requestHistoryButtonId).click(function requestTrack() {
		new HistoryHandler().getUserHistoryData();
		$('#' + historyTableSuccessId).fadeOut('slow');
		$('#' + historyTableFailureId).fadeOut('slow');
		$('#' + historyTableSpaceId).empty();
		$('#' + requestHistoryButtonId).val(_t(refreshHistory));
	});

	$('#' + deleteHistoryButtonId).hide().click(function deleteTrack() {
		new HistoryHandler().deleteUserHistoryData();
		$('#' + historyTableSuccessId).fadeOut('slow');
		$('#' + historyTableFailureId).fadeOut('slow');
		$('#' + requestHistoryButtonId).val(_t(requestHistory));
	});

	$('#' + settingsPasswordInputId).keyup(function passwordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + settingsPasswordInputId),
				$('#' + settingsPasswordMeterId),
				$('#' + settingsPasswordStrengthId),
				settingsPasswordExtras);
		if ($(this).val().length > 0){
			settingsPasswordExtras.fadeIn('slow');
		} else {
			settingsPasswordExtras.fadeOut('slow');
		}
	});

	$('#' + settingsPasswordInfoIconId).click(function passwordInfoIcon() {
		new GuiHandler().showGeneratePasswordPopup();
	});

	$('#' + passwordGeneratorButton).click(function passwordGeneratorButton() {
		new PasswordHandler().generate_password($('#' + passwordGeneratorOutput));
	});

	$('#' + popupPasswordGeneratorButton).click(function passwordGeneratorButton() {
		new PasswordHandler().generate_password($('#' + popupPasswordGeneratorOutput));
	});

	$('#' + clearStatisticsButtonId).click(function clearCtatisticsButton(){
		new StatisticsHandler().deleteStatistics();
	});

	$('#' + infoEditsId).click(function (){
		new StatisticsHandler().getEditsDone();
	});

	$('#' + infoStatementsId).click(function (){
		new StatisticsHandler().getStatementsSend();
	});

	$('#' + infoVoteArgumentsId).click(function (){
		new StatisticsHandler().getArgumentVotes();
	});

	$('#' + infoVoteStatementsId).click(function (){
		new StatisticsHandler().getStatementVotes();
	});

	$('#' + settingsReceiveNotifications).change(function notificationReceiverChange() {
		new SettingsHandler().setUserSetting($(this), 'notification');
	});

	$('#' + settingsReceiveMails).change(function emailReceiverChange() {
		new SettingsHandler().setUserSetting($(this), 'mail');
	});

	$('#' + settingsPublicNick).change(function publicNickChange() {
		new SettingsHandler().setUserSetting($(this), 'public_nick');
	});

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});
});
