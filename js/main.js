
$(document).ready(function () {

    var my_html = '<div style="text-align:center">' +
        '<a href="https://plus.google.com/116164959143674684741/"><img src="/img/social/gplus.png" alt="gplus"/></a>' +
        '<a href="http://www.youtube.com/mchalbe"><img src="/img/social/youtube.png" alt="youtube"/></a>' +
        '<a href="http://www.facebook.com/mchalbe"><img src="/img/social/facebook.png" alt="facebook"/></a>' +
        '<a href="http://www.linkedin.com/pub/matthew-halbe/2b/a37/911/"><img src="/img/social/linkedin.png" alt="linkedin"/></a>' +
        '<a href="http://twitter.com/_yonant"><img src="/img/social/twitter.png" alt="twitter"/></a>' +
        '<a href="https://alpha.app.net/eblah"><img src="/img/social/app_net.png" alt="app_net"/></a>' +
        '<a href="https://kippt.com/mchalbe"><img src="/img/social/kippt.png" alt="kippt"/></a>' +
        '<a href="http://eblahm.appspot.com/rss"><img src="/img/social/rss.png" alt="rss"/></a>' +
        '</div>';
    $('#ptrig').popover({content:my_html, html:true});

    $(".ar").click(function () {
        window.location = $(this).data("url");
    });


    $(".ar").mouseover(function(e) {
        var dbk = $(this).attr('id')
        $(".inner_"+dbk).show();
        $(".holder_"+dbk).hide();
    }).mouseout(function(){
            var dbk = $(this).attr('id')
            $(".inner_"+dbk).hide();
            $(".holder_"+dbk).show();
        });

    var random_picture_key = $("#sidebar_inner").data('random_picture_key');
    var random_picture_path = $("#sidebar_inner").data('random_picture_path');
    var sheight = String(window.innerHeight - $("#my_nav").height());
    var swidth = String($("#sidebar").width());
    var desktop_or_tablet = true
    if ((/iPhone|iPod|Android|BlackBerry/).test(navigator.userAgent)) {
        desktop_or_tablet = false
        pic_url = '/pic?k=' + random_picture_key
    }
    else {
        pic_url = '/pic/sbar?k=' + random_picture_key + '&h=' + sheight + '&w=' + swidth
    }
    $("#sidebar_inner").html('<a href="' + random_picture_path + '"><img id="unique_pic" src="' + pic_url + '"></a>');
    if (desktop_or_tablet) {if (window.screen.width > 768) {$("#unique_pic").css("width", swidth)}};
});