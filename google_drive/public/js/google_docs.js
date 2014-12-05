/* Javascript for GoogleDocumentBlock. */
function GoogleDocumentBlock(runtime, element) {

    var iframe = $('iframe', element);
    if(iframe.length > 0){
        var iframe_src = iframe.attr('src');

        if ((iframe_src.indexOf("document") >= 0) ||
            (iframe_src.indexOf("spreadsheets") >= 0)){
            /* add class to iframe containing Google document or spreadsheet*/
            iframe.addClass('no-width-height');
        }
    }

    function SignalDocumentLoaded(ev, presented_within){
        var document_url = $(ev.target).attr('src');
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'document_loaded'),
            data: JSON.stringify({
                url: document_url,
                displayedin: presented_within
             })
        });
    }
    $('iframe', element).load(function(e){SignalDocumentLoaded(e, 'iframe');});
    $('img', element).load(function(e){SignalDocumentLoaded(e, 'img');});

}
