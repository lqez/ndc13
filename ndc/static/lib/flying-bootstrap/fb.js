// Inspiration from https://github.com/aldomatic/FB-Style-Page-Slide-Menu
$(function(){
    var menuOpened = false;
    var menuDelay = 300;

    $(".btn-collapse").click(function(){
        var menuWidth = $('.nav-collapse .nav').width();
        if(menuOpened != true){             
            $(".nav-collapse").animate({
                width: menuWidth+"px",
            }, menuDelay);
            $("body").animate({
                marginLeft: menuWidth+"px",
                marginRight: "-"+menuWidth+"px",
            }, menuDelay, function(){menuOpened = true});
            return false;
        } else {
            $(".nav-collapse").animate({
                width: 0,
            }, menuDelay, function(){$(this).css("width","");});
            $("body").animate({
                marginLeft: "0px",
                marginRight: "0px",
            }, menuDelay, function(){menuOpened = false});
            return false;
        }
    });
});
