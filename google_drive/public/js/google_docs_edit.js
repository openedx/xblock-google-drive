function GoogleDocumentEditBlock(runtime, element, defaults) {

    var clear_name_button = $('.clear-display-name', element);
    var save_button = $('.save-button', element);
    var validation_alert = $('#validation_alert', element);
    var embed_code_textbox = $('#edit_embed_code', element);
    var xblock_inputs_wrapper = $('#xblock-inputs', element);

    ToggleClearDefaultName();

    IsUrlValid();

    $('.clear-display-name', element).bind('click', function() {
        $(this).addClass('inactive');
        $('#edit_display_name', element).val(defaults.defaultName);
    });

    $('#edit_display_name', element).bind('keyup', function(){
        ToggleClearDefaultName();
    });

    $('#edit_embed_code', element).bind('keyup', function(){
        IsUrlValid();
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    function ToggleClearDefaultName(name, button){
        if ($('#edit_display_name').val() == defaults.defaultName){
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
            'display_name': $('.edit-display-name', element).val(),
            'embed_code': $('.edit-embed-code', element).val(),
        };

        $('.xblock-editor-error-message', element).html();
        $('.xblock-editor-error-message', element).css('display', 'none');
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(false);
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    }

    function IsUrlValid(){
        var embed_html = $("#edit_embed_code", element).val();

        var google_doc = $(embed_html);
        $('#edit_embed_code', element).css({'cursor':'wait'});
        save_button.addClass('disabled').unbind('click');

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'check_url'),
            data: JSON.stringify({url: google_doc.attr("src")}),
            success: function(result) {
                if (result.status_code != 200){
                    validation_alert.removeClass('covered');
                    embed_code_textbox.addClass('error');
                    xblock_inputs_wrapper.addClass('alerted');
                } else {
                    validation_alert.addClass('covered');
                    save_button.removeClass('disabled');
                    embed_code_textbox.removeClass('error');
                    xblock_inputs_wrapper.removeClass('alerted');

                    save_button.bind('click', SaveEditing);
                }
            },
            error: function(result) {
                validation_alert.removeClass('covered');
                save_button.addClass('disabled').unbind('click');
                embed_code_textbox.addClass('error');
                xblock_inputs_wrapper.addClass('alerted');
            },
            complete: function() {
                $('#edit_embed_code', element).css({'cursor':'auto'});
            }
        });
    }
}
