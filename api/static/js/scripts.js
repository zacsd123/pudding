$(document).ready(function () {
    //상단메뉴 고정
    var $header = $('header');
    $(window).scroll(function () { 
        if ($(this).scrollTop() > 0){
            $header.addClass('sticky');
        } else {
            $header.removeClass('sticky');
        }
    });
});

$(selector).width();