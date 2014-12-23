/* Javascript for GoogleDocumentBlock. */
function GoogleDocumentBlock(runtime, element) {

    var iframe = $('iframe', element);
    var image = $('img', element);
    var display_name = $('.google-docs-xblock-wrapper', element).attr('data-display-name');

    if(iframe.length > 0){
        var iframe_src = iframe.attr('src');

        if ((iframe_src.indexOf("document") >= 0) ||
            (iframe_src.indexOf("spreadsheets") >= 0)){
            /* add class to iframe containing Google document or spreadsheet*/
            iframe.addClass('no-width-height');
        }

        iframe.attr('title', display_name);
    }else if(image.length > 0){
        image.attr('alt', display_name);
    }

    function SignalDocumentLoaded(ev, presented_within){
        var document_url = $(ev.target).attr('src');
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'publish_event'),
            data: JSON.stringify({
                url: document_url,
                displayed_in: presented_within,
                event_type: 'edx.googlecomponent.document.displayed',
             })
        });
    }
    iframe.load(function(e){SignalDocumentLoaded(e, 'iframe');});
    image.load(function(e){SignalDocumentLoaded(e, 'img');});

}
