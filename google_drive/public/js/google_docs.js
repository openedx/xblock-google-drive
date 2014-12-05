/* Javascript for GoogleDocumentBlock. */
function GoogleDocumentBlock(runtime, element) {

    $(function ($) {

        var iframe = $('iframe', element);
        if(iframe.length > 0){
            var iframe_src = iframe.attr('src');

            if ((iframe_src.indexOf("document") >= 0) ||
                (iframe_src.indexOf("spreadsheets") >= 0)){
                /* add class to iframe containing Google document or spreadsheet*/
                iframe.addClass('no-width-height');
            }
        }

        $('iframe', element).load(SignalDocumentLoaded('iframe.loaded'));

        $('img', element).load(SignalDocumentLoaded('image.loaded'));

        function SignalDocumentLoaded(event_name){
            var document_url = $(this).attr('src');
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'document_loaded'),
                data: JSON.stringify({url: document_url, eventName: event_name})
            });
        }

    });
}
