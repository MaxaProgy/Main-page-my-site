window.addEventListener("load", function() {
    let date = new Date().getFullYear();
    let year = "";
    if (date > 2022) {
        year = " - " + date;
    }
    document.getElementById("copyright").innerHTML = "© 2022 "+ year + " by M@x@_progy(Зырянова Мария) " +
        "                                                Сайт-портфолио<br>\n" +
        "                We love our users!💙";

    // Функциональность прокрутки
    $(window).scroll( () => {
        var windowTop = $(window).scrollTop();
        windowTop > 100 ? $('nav-base').addClass('navShadow') : $('nav-base').removeClass('navShadow');
        windowTop > 100 ? $('#ul-base').css('top','75px') : $('#ul-base').css('top','75px');
    });

    // Нажмите на логотип, чтобы прокрутить вверх
    $('#logo').on('click', () => {
        $('html,body').animate({
            scrollTop: 0
        },500);
    });

    // Переключить меню
    $('#menu-toggle').on('click', () => {

        $('#menu-toggle').toggleClass('closeMenu');
        $('#ul-base').toggleClass('showMenu');

        $('.li-base').on('click', () => {
            $('#ul-base').removeClass('showMenu');
            $('#menu-toggle').removeClass('closeMenu');
        });
    });


});


document.addEventListener('DOMContentLoaded', function () {
    const slider = new ChiefSlider('.slider', {
        loop: true,
        autoplay: true,
        interval: 5000,
        refresh: true,
    });
});