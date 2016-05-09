$(window).on('load', function() {
    console.log('the page is loaded');
});

$('.widget.follow').on('click', function() {
    console.log('follow was clicked');
    var state = $(this).attr('data-state');
    if (state == 'pending') {
        console.log('request in progress, dropping second click');
        return;
    }
    var checked  = state === 'checked';
    var nextState = checked ? 'unchecked' : 'checked';
    var elt = $(this);
    elt.attr('data-state', 'pending');
    $.ajax('/api/upvote', {
        method: 'POST',
        data: {
            followee: $('.answer.content').attr('data-followee-id'),
            follow: !checked,
            _csrf_token: csrfToken,
        },
        success: function(data) {
            /* called when post succeeds */
            console.log('post succeeded with result %s', data.result);
            elt.attr('data-state', nextState);
        },
        error: function() {
            /* called when post fails */
            console.error('post failed');
            elt.attr('data-state', state);
        }
    });
});
