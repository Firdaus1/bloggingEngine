var tempCity = "",
    tempState = "",
    tempCountry = "";
$(window).on('load', function() {
    console.log('the page is loaded');
});

$.getJSON('https://geoip-db.com/json/geoip.php?jsonp=?')
         .done (function(location)
         {
            tempCountry = location.country_name;
            tempState = location.state;
            tempCity = location.city;
            hello()
         });
function hello(){
   console.log(tempCity);
}

$('.widget.agree').on('click', function() {
    console.log('agree was clicked');
    var state = $(this).attr('data-state');

    var elt = $(this);
    $.ajax('/api/geolocation', {
        method: 'POST',
        data: {
            postId:postId,
            tempCity:tempCity,
            tempCountry:tempCountry,
            tempState:tempState,
            checked: true,
            _csrf_token: csrf_token
        },
        success: function(data) {
            /* called when post succeeds */
            console.log('post succeeded with result %s', data.result);
        },
        error: function() {
            /* called when post fails */
            console.error('post failed');
        }
    });
});

