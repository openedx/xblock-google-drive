/* Javascript for GoogleDocumentBlock. */
function GoogleDocumentBlock(runtime, element) {

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

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
