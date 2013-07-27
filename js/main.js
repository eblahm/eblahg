
$(document).ready(function () {
var loader_gif = '<div style="text-align:center; vertical-align: middle;"><img src="/img/loader.gif" /></div>'
    $('#main_container').on('click', '.show_more', function (event) {
        var offset = $(this).data('offset');
        $(this).hide();
        $(".eb").html(loader_gif)
        $.ajax({
            url: '/?o=' + offset,
            dataType: "html",
            error: function() { $('#feed').append('request failed :(');},
            success: (function (data) {
                $('.eb').html('').removeClass('eb')
                $('#feed').append(data);
            })
        });
    });

    $('#ptrig').popover({content:social_html, html:true});

    $('#main_container').on('click', '.ar', function (event) {
        window.location = $(this).data("url");
    });


    var url = "/pics/" + $("#sidebar_inner").data('key');
    var sheight = String(window.innerHeight - $("#my_nav").height());
    var swidth = String($("#sidebar").width());
    var desktop_or_tablet = true
    if ((/iPhone|iPod|Android|BlackBerry/).test(navigator.userAgent)) {
        desktop_or_tablet = false
        sidebar_pic = url
    }
    else {
        sidebar_pic = url + '?&h=' + sheight + '&w=' + swidth
    }
    $("#sidebar_inner").html('<a href="' + url + '"><img id="unique_pic" src="' + sidebar_pic + '" title="'+ $("#sidebar_inner").data('title') + '"></a>');
    if (desktop_or_tablet) {if (window.screen.width > 768) {$("#unique_pic").css("width", swidth)}};





});
