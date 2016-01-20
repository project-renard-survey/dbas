/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 06.01.16
 */

function DiscussionIsland(){

	/**
	 * Displays the island of current discussion
	 */
	this.showIsland = function(){

		var url = window.location.href,
			splits = url.split('/');
		this.getAllArgumentsForIslandView(splits[6])
	};

	/**
	 * Ajax request for the island view
	 * @param arg_uid int
	 */
	this.getAllArgumentsForIslandView = function(arg_uid){
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), settings_data, url;
		$.ajax({
			url: 'ajax_get_everything_for_island_view',
			method: 'GET',
			dataType: 'json',
			data: { lang: getLanguage(), arg_uid: arg_uid },
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new DiscussionIsland().callbackIfDoneAllArgumentsForIslandView(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
			new GuiHandler().hideErrorDescription();
		}).fail(function ajaxGetAllUsersFail() {
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 16). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Callback for the island view
	 * @param data
	 */
	this.callbackIfDoneAllArgumentsForIslandView = function (data){
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + popupEditStatementErrorDescriptionId).text(_t(noIslandView));
			$('#' + scStyleIslandId).attr('checked', true).prop('checked', true);
			$('#' + scStyleDialogId).attr('checked', false).prop('checked', false);
			$('#' + scStyleCompleteId).attr('checked', false).prop('checked', false);
			this.styleButtonChanged(scStyleDialogId);
		} else {
			$('#' + discussionFailureRowId).hide();
			new DiscussionIsland().displayDataInIslandView(parsedData);
		}
	};

	/**
	 * Displays given data in the island view
	 * @param jsonData json encoded dictionary
	 */
	this.displayDataInIslandView = function (jsonData) {
		var div, row, header, islandViewContainerSpace = $('#' + islandViewContainerSpaceId), helper = new Helper(),
				titles = [];// = helper.createRelationsTextWithoutConfrontation(jsonData.premise, jsonData.conclusion, false); //  # todo server side
		// title order = [undermine, support, undercut, overbid, rebut, noopinion]
		islandViewContainerSpace.empty();
		titles[0] = jsonData.undermine_text;
		titles[1] = jsonData.support_text;
		titles[2] = jsonData.undercut_text;
		titles[3] = jsonData.overbid_text;
		titles[4] = jsonData.rebut_text;

		// first row with header only
		row = $('<div>').addClass('row').attr({style: 'padding-left: 15px; padding-right: 15px;'});
		div = $('<div>').addClass('col-md-12');
		header = '<h4>' + _t(islandView) + ' ' + _t(forText) + ' <strong>' + jsonData.argument + '.</strong></h4>';
		div.append(header);
		row.append(div);
		islandViewContainerSpace.append(row);

		// second row with supports and undermines
		row = $('<div>').addClass('row').attr({style: 'padding-left: 15px; padding-right: 15px;'});
		// con premise - undermines
		this.createPartOfIsland('6', row, false, ballot, titles[0], jsonData, 'undermines');
		islandViewContainerSpace.append(row);
		// pro premise - supports
		this.createPartOfIsland('6', row, true, checkmark, titles[1], jsonData, 'supports');

		// third row with overbids and undercuty
		row = $('<div>').addClass('row').attr({style: 'padding-left: 15px; padding-right: 15px;'});
		// con relation - undercuts
		this.createPartOfIsland('6', row, false, ballot, titles[2], jsonData, 'undercuts');
		islandViewContainerSpace.append(row);
		// pro relation - overbids
		this.createPartOfIsland('6', row, true, checkmark, titles[3], jsonData, 'overbids');

		// last row with rebuts
		row = $('<div>').addClass('row').attr({style: 'padding-left: 15px; padding-right: 15px;'});
		// con conclusion - rebuts
		this.createPartOfIsland('12', row, false, ballot, titles[4], jsonData, 'rebuts');
		islandViewContainerSpace.append(row);

		// add argument button
		div = "<div class='center text-center'>";
		div += "<input id='island-view-add-arguments' type='button' value='" + _t(addStatements);
		div += "' class='button button-block btn btn-primary' data-dismiss='modal'/>";
		div += "</div>";
		islandViewContainerSpace.append(div);
		$('#island-view-add-arguments').click(function(){
			var i, ul = $('<ul>').css('list-style-type', 'none').css('padding-left','0px'), input, li, h = new Helper();
			for (i=0; i<5; i++){
				li = $('<li>').attr({id: 'li_add_island_' + i});
				input = $('<input>').attr({id: 'island_' + i, type: 'radio', value: titles[i], name: radioButtonGroup});
				li.html(h.getFullHtmlTextOf(input) + '<label title="' + titles[i] + '" for="' + 'island_' + i + '" style="width:95%;">' + titles[i] + '</label>');
				ul.append(li);
			}
			// displayConfirmationDialogWithoutCancelAndFunction(_t(addStatements), helper.getFullHtmlTextOf(ul));
		}).addClass('disabled');
	};

	/**
	 * Creates on box in the island view
	 * @param colSize 6 or 12 as string
	 * @param row <row>
	 * @param isSupport
	 * @param sign ballot, checkmark, whatever
	 * @param title of the box
	 * @param data as json
	 * @param valueName of the attack
	 */
	this.createPartOfIsland = function(colSize, row, isSupport, sign, title, data, valueName){
		var div, div_panel, div_header, div_body;
		div = $('<div>').addClass('col-md-' + colSize);
		// version with panel
		/*
		header = '<h5><span class="' + color + '-bg text-center">' + sign + '</span> ' + title + '</h5>';
		div.append(header);
		div.append(data[valueName] > 0 ? new Helper().getValuesOfDictWithPrefixAsUL(data, valueName) : '<label>' + _t(noEntries) + '</label>');
		*/
		// version with panel
		div_panel = $('<div>').addClass('panel').addClass('panel-default');
		div_header = $('<div>').addClass('panel-heading').append('<h5><span class="' + (isSupport? 'text-success' : 'text-danger')
			+ ' text-center">' + sign + '</span> ' + title + '</h5>');
		div_body = $('<div>').addClass('panel-body').append(data[valueName] > 0 ?
			new Helper().getValuesOfDictWithPrefixAsUL(data, valueName) :
			'<label>' + _t(noEntries) + '</label>');
		div_panel.append(div_header);
		div_panel.append(div_body);
		div.append(div_panel);
		row.append(div);
	}
}