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

        $('iframe', element).load(function(){
            var iframe_url = $(this).attr('src');
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'iframe_loaded'),
                data: JSON.stringify({url: iframe_url})
            });
        });

        $('img', element).load(function(){
            var image_url = $(this).attr('src');
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'image_loaded'),
                data: JSON.stringify({url: image_url})
            });
        });

    });
}
