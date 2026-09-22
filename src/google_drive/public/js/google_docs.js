/* Javascript for GoogleDocumentBlock. */
function GoogleDocumentBlock(runtime, element) {
    var iframe = $('iframe', element);
    var image = $('img', element);
    var xblock_wrapper = $('.google-docs-xblock-wrapper', element);
    var display_name = xblock_wrapper.attr('data-display-name');
    var alt_text = xblock_wrapper.attr('data-alt-text');

    if(iframe.length > 0){
        var iframe_src = iframe.attr('src');

        if ((iframe_src.indexOf("document") >= 0) ||
            (iframe_src.indexOf("spreadsheets") >= 0)){
            /* add class to iframe containing Google document or spreadsheet*/
            iframe.addClass('no-width-height');
        }

        iframe.attr('title', display_name);
    }else if(image.length > 0){
        image.attr('alt', alt_text);
    }

    function SignalDocumentLoaded(ev, presented_within){
        var document_url = $(ev.target).attr('src');
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'publish_event'),
            data: JSON.stringify({
                url: document_url,
                displayed_in: presented_within,
                event_type: 'edx.googlecomponent.document.displayed'
            }),
            success: function(){
                $('.load_event_complete', element).val("I've published the event that indicates that the load has completed");
            }
        });
    }

    iframe.load(function(e){SignalDocumentLoaded(e, 'iframe');});
    image.load(function(e){SignalDocumentLoaded(e, 'img');});

}
