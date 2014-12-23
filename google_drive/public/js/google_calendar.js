/* Javascript for GoogleDocumentBlock. */
function GoogleCalendarBlock(runtime, element) {

    $('iframe', element).load(function(){
        var iframe_url = $(this).attr('src');
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'publish_event'),
            data: JSON.stringify({url: iframe_url, displayed_in: 'iframe', event_type: 'edx.googlecomponent.calendar.displayed'})
        });
    });
}
