function GoogleCalendarEditBlock(runtime, element, defaults) {

    var clear_name_button = $('.clear-display-name', element);
    var clear_id_button = $('.clear-calendar-id', element);
    var save_button = $('.save-button', element);
    var validation_alert = $('#validation_alert', element);
    var xblock_inputs_wrapper = $('#xblock-inputs', element);
    var edit_calendar_id_input = $('#edit_calendar_id', element);
    var edit_display_name_input = $('#edit_display_name', element);
    var error_message_div = $('.xblock-editor-error-message', element);

    ToggleClearDefaultName();
    ToggleClearCalendarID();

    $('.clear-display-name', element).bind('click', function() {
        $(this).addClass('inactive');
        edit_display_name_input.val(defaults.defaultName);
    });

    edit_display_name_input.bind('keyup', function(){
        ToggleClearDefaultName();
    });

    $('.clear-calendar-id', element).bind('click', function() {
        $(this).addClass('inactive');
        edit_calendar_id_input.val(defaults.defaultID);
        save_button.unbind('click').bind('click', SaveEditing);

        if (!validation_alert.hasClass('covered')) {
            validation_alert.addClass('covered');
            save_button.removeClass('disabled');
            edit_calendar_id_input.removeClass('error');
            xblock_inputs_wrapper.removeClass('alerted');

            save_button.bind('click', SaveEditing);
        }
    });

    edit_calendar_id_input.bind('keyup', function(){
        ToggleClearCalendarID();


        var inputVal = $(this).val();
        var calendarIDReg = /[\w-\.]+@+[\w-\.]/;
        if(!calendarIDReg.test(inputVal)) {
            save_button.addClass('disabled').unbind('click');
            validation_alert.removeClass('covered');
            $(this).addClass('error');
            xblock_inputs_wrapper.addClass('alerted');
        } else {
            validation_alert.addClass('covered');
            save_button.removeClass('disabled');
            $(this).removeClass('error');
            xblock_inputs_wrapper.removeClass('alerted');

            save_button.bind('click', SaveEditing);
        }
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    function ToggleClearDefaultName(){
        if (edit_display_name_input.val() == defaults.defaultName){
            if (!clear_name_button.hasClass('inactive')){
                clear_name_button.addClass('inactive');
            }
        }
        else {
            clear_name_button.removeClass('inactive');
        }
    }

    function ToggleClearCalendarID(){
        if (edit_calendar_id_input.val() == defaults.defaultID){
            if (!clear_id_button.hasClass('inactive')){
                clear_id_button.addClass('inactive');
            }
        }
        else {
            clear_id_button.removeClass('inactive');
        }
    }

    function SaveEditing(){
        var data = {
            'display_name': edit_display_name_input.val(),
            'calendar_id': edit_calendar_id_input.val(),
            'default_view': $('select.edit-label_type > option:selected', element).val(),
        };

        error_message_div.html();
        error_message_div.css('display', 'none');
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(false);
            } else {
                error_message_div.html('Error: '+response.message);
                error_message_div.css('display', 'block');
            }
        });
    }
}
