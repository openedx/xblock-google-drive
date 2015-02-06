function GoogleDocumentEditBlock(runtime, element) {
    var clear_name_button = $('.clear-display-name', element);
    var save_button = $('.save-button', element);
    var validation_alert = $('.validation_alert', element);
    var embed_code_textbox = $('#edit_embed_code', element);
    var xblock_inputs_wrapper = $('.xblock-inputs', element);
    var edit_display_name_input = $('#edit_display_name', element);
    var error_message_div = $('.xblock-editor-error-message', element);
    var defaultName = edit_display_name_input.attr('data-default-value');
    var edit_alt_text_input = $('#edit_alt_text', element);
    var alt_text_item = $('li#alt_text_item', element);

    ToggleClearDefaultName();
    IsUrlValid();

    $('.clear-display-name', element).bind('click', function() {
        $(this).addClass('inactive');
        edit_display_name_input.val(defaultName);
    });

    edit_display_name_input.bind('keyup', function(){
        ToggleClearDefaultName();
    });

    $('#edit_embed_code', element).bind('keyup', function(){
        IsUrlValid();
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    function ToggleClearDefaultName(name, button){
        if (edit_display_name_input.val() == defaultName){
            if (!clear_name_button.hasClass('inactive')){
                clear_name_button.addClass('inactive');
            }
        }
        else {
            clear_name_button.removeClass('inactive');
        }
    }

    function SaveEditing(){
        var data = {
            'display_name': edit_display_name_input.val(),
            'embed_code': embed_code_textbox.val(),
            'alt_text': edit_alt_text_input.val(),
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

    function HideAltTextInput(){
        edit_alt_text_input.val('');
        alt_text_item.addClass('covered');
    }

    function IsUrlValid(){
        var embed_html = embed_code_textbox.val();

        var google_doc = $(embed_html);
        embed_code_textbox.css({'cursor':'wait'});
        save_button.addClass('disabled').unbind('click');

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'check_url'),
            data: JSON.stringify({url: google_doc.attr("src")}),
            success: function(result) {
                if (result.status_code >= 400){
                    validation_alert.removeClass('covered');
                    embed_code_textbox.addClass('error');
                    xblock_inputs_wrapper.addClass('alerted');
                    HideAltTextInput();
                } else {
                    validation_alert.addClass('covered');
                    save_button.removeClass('disabled');
                    embed_code_textbox.removeClass('error');
                    xblock_inputs_wrapper.removeClass('alerted');

                    save_button.bind('click', SaveEditing);

                    if (embed_html.toLowerCase().indexOf("<img") >= 0){
                        if (alt_text_item.hasClass('covered')){
                            alt_text_item.removeClass('covered');
                        }
                    } else {
                        if (!alt_text_item.hasClass('covered')){
                            HideAltTextInput();
                        }
                    }
                }
            },
            error: function(result) {
                validation_alert.removeClass('covered');
                save_button.addClass('disabled').unbind('click');
                embed_code_textbox.addClass('error');
                xblock_inputs_wrapper.addClass('alerted');
            },
            complete: function() {
                embed_code_textbox.css({'cursor':'auto'});
            }
        });
    }
}
