$('.message a').click(function(e){
    e.preventDefault();
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    return false;
});