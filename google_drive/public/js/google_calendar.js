/* Javascript for GoogleDocumentBlock. */
function GoogleCalendarBlock(runtime, element) {

    $('iframe', element).load(function(){
        var iframe_url = $(this).attr('src');
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'publish_event'),
            data: JSON.stringify({url: iframe_url, displayedin: 'iframe', event_name: 'edx.googlecomponent.calendar.displayed'})
        });
    });
}
