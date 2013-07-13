
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

    var random_picture_id = $("#sidebar_inner").data('random_picture_id');
    var sheight = String(window.innerHeight - $("#my_nav").height());
    var swidth = String($("#sidebar").width());
    var desktop_or_tablet = true
    if ((/iPhone|iPod|Android|BlackBerry/).test(navigator.userAgent)) {
        desktop_or_tablet = false
        sidebar_pic = '/pics/' + random_picture_id
    }
    else {
        sidebar_pic = '/pics/' + random_picture_id + '?&h=' + sheight + '&w=' + swidth
    }
    $("#sidebar_inner").html('<a href="/pics/' + random_picture_id + '"><img id="unique_pic" src="' + sidebar_pic + '"></a>');
    if (desktop_or_tablet) {if (window.screen.width > 768) {$("#unique_pic").css("width", swidth)}};
});
