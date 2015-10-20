/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function JsonGuiHandler() {
	'use strict';

	/**
	 * Sets given json content as start statement buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartStatement = function (jsonData) {
		var listitems = [], guihandler = new GuiHandler(), helper = new Helper();
		guihandler.setDiscussionsDescription(_t(startDiscussionText), '' , null);
		$.each(jsonData.statements, function setJsonDataToContentAsConclusionEach(key, val) {
			listitems.push(helper.getKeyValAsInputInLiWithType(val.uid, val.text + '.', true, false, false, ''));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			// todo: is this even used?
			alert('discussion-guihandler.: setJsonDataToContentAsStartStatement');
			guihandler.setDiscussionsDescription(_t(firstOneText) + '<b>' + jsonData.statements.currentStatementText + '</b>', '' , null);
		}

		if (typeof jsonData.logged_in == "string") {
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(newConclusionRadioButtonText), false, false, false, ''));
		}

		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given json content as start premisses buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartPremisses = function (jsonData) {
		var listitems = [],
			guihandler = new GuiHandler(),
			text,
			firstOne = true,
			helper = new Helper(),
			attributes,
			index, dict;

		text = helper.startWithLowerCase(jsonData.currentStatement.text);
		dict =  {'text': text, 'conclusion_id': jsonData.conclusion_id};
		guihandler.setDiscussionsDescription(_t(sentencesOpenersRequesting[0]) + ' <b>' + text + '</b> ?', text, dict);

		$.each(jsonData.premisses, function setJsonDataToContentAsConclusionEach(key, val) {
			text = '';
			index = 0;
			attributes = {};
			$.each(val, function setJsonDataToContentAsConclusionEachVal(valkey, valval) {
				if (text=='')
					text = _t(because) + ' ';
				else
					text += ' <i>and</i> ' + helper.startWithLowerCase(_t(because)) + ' ';

				text += helper.startWithLowerCase(valval.text);
				firstOne = false;
				index += 1;
				attributes['text_' + index + '_statement_id'] = valkey;
				attributes['text_' + index] = valval.text + '.';
			});
			text += '.';
			attributes['text_count'] = index;
			// we are saving the group id ad key
			listitems.push(helper.getKeyValAsInputInLiWithType(key, text, false, true, false, text, attributes));
		});

		if (typeof jsonData.logged_in == "string") {
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, firstOne ? _t(addPremisseRadioButtonText) : _t(newPremisseRadioButtonText), false, false, false, ''));
		}

		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontation = function (jsonData) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premisse = jsonData.premisse_text,
			opinion,
			confrontationText,
			listitems = [],
			dict,
			confrontation = jsonData.confrontation.substring(0, jsonData.confrontation.length),
			confronation_id = '_argument_' + jsonData.confrontation_argument_id,
			argument_id = '_argument_' + jsonData.argument_id,
			relationArray = helper.createConfrontationsRelationsText(confrontation, conclusion, premisse, false, true);

		//alert(jsonData.confrontation_uid + "\n" + jsonData.confrontation_argument_id);

		if (typeof jsonData.relation == 'undefined'){
			opinion = '<b>' + conclusion + ', ' + helper.startWithLowerCase(_t(because)) + ' ' + premisse + '</b>';
		} else {
			opinion = '<b>' + conclusion + '</b> ' + jsonData.relation + 's ' + '<b>' + premisse + '</b>';
		}

		// build some confrontation text
		if (jsonData.attack == 'undermine'){
			confrontationText = _t(otherParticipantsThinkThat) + ' <b>' + premisse + '</b> ' + _t(doesNotHoldBecause) + ' ';
		} else if (jsonData.attack == 'rebut'){
			confrontationText = _t(otherParticipantsAcceptBut) + ' ' + _t(strongerStatementForRecjecting) + ' <b>' + conclusion + '</b>.' +
				' They say: ';
		} else if (jsonData.attack == 'undercut'){
			confrontationText = _t(otherParticipantsThinkThat) + ' <b>' + premisse + '</b> ' + _t(doesNotJustify) + ' <b>' + conclusion + '</b>,' +
				' ' + _t(because) + ' ';
		}
		confrontationText += '<b>' + confrontation + '</b>. [<i>' + jsonData.attack + '</i>]';

		// set discussions text
		dict = {confrontation_uid: jsonData.confrontation_uid,
				current_attack: jsonData.attack};
		guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ' ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + _t(whatDoYouThink),
			'This confrontation is a ' + jsonData.attack, dict);

		// build the radio buttons
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undermine + confronation_id, relationArray[0] + ' [<i>undermine</i>]', false, false, true, attr_undermine));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_support + confronation_id, relationArray[1] + ' [<i>support</i>]', false, false, true, attr_support));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undercut + confronation_id, relationArray[2] + ' [<i>undercut</i>]', false, false, true, attr_undercut));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_overbid + confronation_id, relationArray[3] + ' [<i>overbid</i>]', false, false, true, attr_overbid));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_rebut + argument_id, relationArray[4] + ' [<i>rebut</i>]', false, false, true, attr_rebut));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_no_opinion + argument_id, relationArray[5] + ' [<i>noopinion</i>]', false, false, true, attr_no_opinion));
		// TODO HOW TO INSERT ATTACKING PREMISEGROUPS?

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontationWithoutConfrontation = function (jsonData) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premisse = jsonData.premisse_text,
			opinion,
			confrontationText,
			listitems = [],
			dict,
			relation = jsonData.relation,
			conclusion_uid = jsonData.conclusion_uid,
			argument_uid = jsonData.argument_uid,
			premissegroup_uid = jsonData.premissegroup_uid;

		if (typeof relation == 'undefined'){
			opinion = '<b>' + conclusion + ', ' + helper.startWithLowerCase(_t(because)) + ' ' + premisse + '</b>';
		} else {
			opinion = '<b>' + premisse + '</b> ' + relation + 's ' + '<b>' + conclusion + '</b>';
		}

		// build some confrontation text
		confrontationText = _t(otherParticipantsDontHave) + ' <b>' + premisse + '</b>';

		// set discussions text
		dict = { // todo params in id.js!
			'text': premisse,
			'attack': relation,
			'related_argument': argument_uid,
			'premissegroup_uid': premissegroup_uid,
			'conclusion_id': conclusion_uid};

		guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ' ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + _t(whatDoYouThink),
			'This confrontation is a ' + jsonData.attack, dict);

		// build the radio buttons
		// TODO HOW TO INSERT THINGS FOR PGROUP ' + jsonData.premissesgroup_uid + '?</u></i></b>
		// TODO BUTTONS ARE DEPENDING ON THE ATTACK?</u></i></b>
		if (typeof jsonData.logged_in == "string") {
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(addArgumentRadioButtonText), false, false, false, _t(addArgumentRadioButtonText)));
		} else {
			guihandler.setErrorDescription(_t(discussionEnd) + '<br>' + _t(clickHereForRegistration));
			guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ' ' + opinion + '.<br><br>'
			+ confrontationText + '.',
			'This confrontation is a ' + jsonData.attack, dict);
		}

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontationReasoning = function (jsonData){
		var premisse = jsonData.premissegroup.replace('.',''),
			helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			relationArray = helper.createRelationsText(jsonData.confrontation_text, premisse, conclusion, true, false),
			text, listitems = [], i, reason, id, long_id, dict;

		if (jsonData.relation === attr_undermine) {			text = relationArray[0] + '. ' + _t(canYouGiveAReason) + ' (' + _t(youMadeAn) + ' ' + attr_undermine + ')';
		} else if (jsonData.relation === attr_support) {	text = relationArray[1] + '. ' + _t(canYouGiveAReason) + ' (' + _t(youMadeA) + ' ' + attr_support + ')';
		} else if (jsonData.relation === attr_undercut) {	text = relationArray[2] + '. ' + _t(canYouGiveAReason) + ' (' + _t(youMadeAn) + ' ' + attr_undercut + ')';
		} else if (jsonData.relation === attr_overbid) {	text = relationArray[3] + '. ' + _t(canYouGiveAReason) + ' (' + _t(youMadeAn) + ' ' + attr_overbid + ')';
		} else if (jsonData.relation === attr_rebut) {		text = relationArray[4] + ', ' + _t(butWhich) + '?'	   + ' (' + _t(youMadeA) + ' ' + attr_rebut + ')';
		}

		for (i=0; i<parseInt(jsonData.reason); i++){
			long_id = jsonData.relation + '_' + jsonData.type + '_' + jsonData['reason' + i + 'id'];
			id = jsonData['reason' + i + '_statement_id'];
			reason = _t(because) + ' ' + helper.startWithLowerCase(jsonData['reason' + i]) + '.';
			listitems.push(helper.getKeyValAsInputInLiWithType(id, reason, false, true, true, reason, {'long_id': long_id}));
		}

		dict = { // todo params in id.js!
			'text': premisse,
			'attack': jsonData.relation,
			'related_argument': jsonData.argument_uid,
			'premissegroup_uid': jsonData.premissegroup_uid,
			'conclusion_id': jsonData.conclusion_uid,
			'last_relation': jsonData.last_relation,
			'confrontation_text': jsonData.confrontation_text,
			'confrontation_uid': jsonData.confrontation_uid};
		guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ' ' + text, '', dict);

		if (typeof jsonData.logged_in == "string") {
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(addPremisseRadioButtonText), false, false, false, _t(addPremisseRadioButtonText)));
		} else if (parseInt(jsonData.reason) == 0){
			guihandler.setErrorDescription(_t(discussionEnd) + '<br>' + _t(clickHereForRegistration));
		}
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Adds given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.addJsonDataToContentAsArguments = function (jsonData) {
		var text, helper = new Helper();
		$.each(jsonData, function addJsonDataToContentAsArgumentsEach(key, val) {
			// we only want attacking arguments
			if (val.is_supportive === '0') {
				if (val.text.toLowerCase() !== helper.startWithLowerCase(_t(because))) {
					text = _t(because) + ' ' + helper.start(val.text);
				} else {
					text = val.text;
				}
				$('#li_' + addReasonButtonId).before(helper.getKeyValAsInputInLiWithType(val.uid, text, true));
			}
		});

		// hover style element for the list elements
		$('#' + argumentListId).children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonUserDataToAdminContent = function (jsonData) {
		var tableElement, trElement, tbody, thead, tdElement, spanElement, i;
		tdElement = ['', '', '', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-condensed tablesorter',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});

		trElement = $('<tr>');
		tbody = $('<tbody>');
		thead = $('<thead>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text('uid');
		spanElement[1].text(_t(firstname));
		spanElement[2].text(_t(surname));
		spanElement[3].text(_t(nickname));
		spanElement[4].text(_t(email));
		spanElement[5].text(_t(group_uid));
		spanElement[6].text(_t(last_action));
		spanElement[7].text(_t(last_login));
		spanElement[8].text(_t(registered));
		spanElement[9].text(_t(gender));

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			thead.append(trElement);
		}
		tableElement.append(thead);

		// add each user element
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.uid);
			tdElement[1].text(value.firstname);
			tdElement[2].text(value.surname);
			tdElement[3].text(value.nickname);
			tdElement[4].text(value.email);
			tdElement[5].text(value.group_uid);
			tdElement[6].text(value.last_action);
			tdElement[7].text(value.last_login);
			tdElement[8].text(value.registered);
			tdElement[9].text(value.gender);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('table-hover');
			});
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForUsersId).empty().append(tableElement);
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonAttackDataToAdminContent = function (jsonData) {
		var tableElement, trElement, tdElement, tbody, thead, spanElement, i, attacks = [], counter;

		tdElement = ['', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-condensed tablesorter',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});
		tbody = $('<tbody>');
		thead = $('<thead>');

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text(_t(uid));
		spanElement[1].text(_t(text));
		counter = 2;
		$.each(jsonData.attacks, function setJsonAttackDataToAdminContentEach(key, value) {
			spanElement[counter].text(value);
			attacks[(counter-2)] = value;
			counter += 1;
		});

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			thead.append(trElement);
		}
		tableElement.append(thead);

		// add each attack element
		$.each(jsonData, function setJsonAttackDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.id);
			tdElement[1].text(value.text);
			tdElement[2].text(value[attacks[0]]);
			tdElement[3].text(value[attacks[1]]);
			tdElement[4].text(value[attacks[2]]);
			tdElement[5].text(value[attacks[3]]);
			tdElement[6].text(value[attacks[4]]);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('table-hover');
			});
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForAttacksId).empty().append(tableElement);
	};

}