
$(document).ready(function () {

    $('#ptrig').popover({content:social_html, html:true});

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
