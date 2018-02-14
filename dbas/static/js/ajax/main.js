/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

/**
 * Use this to call any url asyncronously
 *
 * @param url to call
 * @param method POST or GET
 * @param data for the body, will be json-decoded
 * @param ajaxDone is the function to call after ajax is done
 * @param ajaxFail is the fucntion to call on fail
 */
function ajaxSkeleton(url, method, data, ajaxDone, ajaxFail){
	'use strict';
	var csrf_token = $('#' + hiddenCSRFTokenId).val();
	$.ajax({
		url: url,
		method: method,
		dataType: 'json',
		contentType: 'application/json',
		data: JSON.stringify(data),
		headers: {'X-CSRF-Token': csrf_token}
	}).done(ajaxDone(data)).fail(ajaxFail());
}

function AjaxMainHandler(){
	'use strict';

	/**
	 * Sends a request for language change
	 * @param new_lang is the shortcut for the language
	 */
	this.switchDisplayLanguage = function (new_lang){
		var url = mainpage + 'ajax_switch_language';
		var data = {'lang': new_lang};
		var done = function ajaxSwitchDisplayLanguageDone() {
			setAnalyticsOptOutLink(new_lang);
			location.reload(true);
		};
		var fail = function ajaxSwitchDisplayLanguageFail(xhr) {
			if (xhr.status === 400) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedBadToken));
			} else if (xhr.status === 500) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedInternalError));
			} else {
				setGlobalErrorHandler(_t(ohsnap), _t(languageCouldNotBeSwitched));
			}
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};

	/**
	 *
	 */
	this.login = function(user, password, showGlobalError){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var url = window.location.href;
        var keep_login = $('#keep-login-box').prop('checked');
		$('#' + popupLoginFailed).hide();
		$('#' + popupLoginFailed + '-message').text('');
		$('#' + popupLoginInfo).hide();
		$('#' + popupLoginInfo + '-message').text('');

		$.ajax({
			url: mainpage + 'ajax_user_login',
			type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
				user: user,
				password: password,
                redirect_url: url,
				keep_login: keep_login
            }),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLoginDone(data) {
			callbackIfDoneForLogin(data, showGlobalError);
		}).fail(function ajaxLoginFail(xhr) {
			var errorMsg = '';

			if (xhr.status === 200) {
				location.reload(true);
			} else if (xhr.status === 302) {
				location.href = xhr.getResponseHeader('Location');
			} else if (xhr.status === 400) {
				errorMsg = _t(requestFailedBadToken);
			} else if (xhr.status === 500) {
				errorMsg = _t(requestFailedInternalError);
			} else {
				errorMsg = _t(requestFailed);
			}

			if (errorMsg.length > 0){
				if (showGlobalError) {
					setGlobalErrorHandler('Ohh!', errorMsg);
				} else {
					$('#' + popupLoginFailed).show();
					$('#' + popupLoginFailed + '-message').html(errorMsg);
				}
			}
		}).always(function ajaxLoginAlways(){
			$('#' + loginPwId).val('');
		});
	};

	/**
	 *
	 * @param service
	 * @param url
	 */
	this.oauthLogin = function(service, url){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$('#' + popupLoginFailed).hide();
		$('#' + popupLoginFailed + '-message').text('');
		$('#' + popupLoginInfo).hide();
		$('#' + popupLoginInfo + '-message').text('');

		$.ajax({
			url: mainpage + 'ajax_user_login_oauth',
			type: 'POST',
			data: {
				service: service,
				redirect_uri: url},
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxOauthLoginDone(data) {
			if (data.error.length !== 0){
				setGlobalErrorHandler('Ohh!', data.error);
			} else if ('missing' in data && data.missing.length !== 0) {
				new GuiHandler().showCompleteLoginPopup(data);
			} else if ('authorization_url' in data && data.authorization_url !== 0){
				window.open(data.authorization_url, '_self');
			}
		}).fail(function ajaxOauthLoginFail(xhr) {
			if (xhr.status === 0 || xhr.status === 200) {
				location.reload(true);
			} else{
				setGlobalErrorHandler('Ohh!', _t(requestFailedInternalError) + ' (' + xhr.status + ')');
			}
		});
	};

	/**
	 *
	 */
	this.logout = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: mainpage + 'ajax_user_logout',
			type: 'POST',
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLogoutDone() {
			location.reload(true);
		}).fail(function ajaxLogoutFail(xhr) {
			if (xhr.status === 200) {
				if (window.location.href.indexOf('settings') !== 0){
					window.location.href = mainpage + 'discuss';
				} else {
					location.reload(true);
				}
			} else if (xhr.status === 403) {
				window.location.href = mainpage + 'discuss';
			} else {
				location.reload(true);
			}
		});
	};

	/**
	 *
	 */
	this.registration = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var firstname = $('#userfirstname-input').val(),
			lastname = $('#userlastname-input').val(),
			nickname = $('#nick-input').val(),
			email = $('#email-input').val(),
			password = $('#' + popupLoginPasswordInputId).val(),
			passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val(),
			recaptcha = $('#recaptcha-token').value,
			gender = '';

		if ($('#' + popupLoginInlineRadioGenderN).is(':checked')){ gender = 'n'; }
		if ($('#' + popupLoginInlineRadioGenderM).is(':checked')){ gender = 'm'; }
		if ($('#' + popupLoginInlineRadioGenderF).is(':checked')){ gender = 'f'; }

		$.ajax({
			url: 'ajax_user_registration',
			type: 'POST',
			data: {
				firstname: firstname,
				lastname: lastname,
				nickname: nickname,
				gender: gender,
				email: email,
				password: password,
				passwordconfirm: passwordconfirm,
				'g-recaptcha-response': recaptcha,
				lang: getLanguage(),
				mode: 'manually'
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRegistrationDone(data) {
			callbackIfDoneForRegistration(data);
		}).fail(function ajaxRegistrationFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status === 400) {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status === 500) {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		}).always(function ajaxLoginAlways(){
			$('#' + popupLoginPasswordInputId).val('');
			$('#' + popupLoginPasswordconfirmInputId).val('');
		});
	};

	/**
	 *
	 */
	this.passwordRequest = function(){
		var email = $('#password-request-email-input').val();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_user_password_request',
			type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: email,
                ui_locales: getLanguage()
            }),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxPasswordRequestDone(data) {
			callbackIfDoneForPasswordRequest(data);
		}).fail(function ajaxPasswordRequestFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status === 400) {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status === 500) {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {
				$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		});
	};

	/**
	 * Get-Request for an roundhouse kick
	 */
	this.roundhouseKick = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'chuck'},
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRoundhouseKickDone(data) {
			if (data.type === 'success'){
				displayConfirmationDialogWithoutCancelAndFunction('Chuck Norris Fact #' + data.value.id,
					'<p>' + data.value.joke + '</p>' +
					'<p class="pull-right">powered by <a href="http://www.icndb.com/" target="_blank">http://www.icndb.com/</a></p>');

			}
		});
	};

	/**
	 * Get your mama
	 */
	this.ajaxMama = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'mama'},
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxMamaDone(data) {
			displayConfirmationDialogWithoutCancelAndFunction('Yo Mamma',  '<h4>' + data.joke + '</h4>\n\n<span' +
					' style="float:right;">powered by <a href="http://yomomma.info/">http://yomomma.info/</a></span>');
		});
	};
}
