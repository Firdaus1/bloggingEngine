function sendMessage(recip, button) {
    if (button.attr('disabled')) return;

    var state = $(this).attr('data-state');
    $.ajax('/hai/send', {
        data: {
            initiator_id: authUserId,
            recipient_id: recip,
            _csrf_token: csrfToken
        },
        method: 'POST',
        success: function(response) {
            button.removeClass('pending');
            addHai(response);
        },
        error: function(err) {
            button.removeClass('pending');
            button.addClass('failed');
        }
    });
    button.addClass('pending');
}

// Global variable storing template for new Hais
var haiTmpl = '<div class="message sent" data-message-id="{{ message_id }}" data-sender-id="{{ sender.id }}">\n  <img class="avatar" src="https://www.gravatar.com/avatar/{{ sender.grav_hash }}">\n  <h2>To <a href="/u/{{ recipient.id }}">{{ recipient.name }}</a></h2>\n  Hai!\n  <div class="timestamp">{{ timestamp }}</div>\n</div>'
/**
 * Add a new Hai to the timeline on the current page.  For convenience, we assume
 * that the Hai is <strong>after</strong> any Hai currently in the timeline.
 * @param hai The Hai to add.
 */
function addHai(hai) {
    // combine template with hai data to make HTML
    var msg = Mustache.render(haiTmpl, hai);
    console.log('generated HTML: %s', msg);
    // add HTML to timeline
    $('#timeline').prepend(msg);
}

$('.message .hai.reply').on('click', function() {
    var recipient = $(this).parent().attr('data-sender-id');
    sendMessage(recipient, $(this));
});