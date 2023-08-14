$(document).ready(function() {

    // Gets the video src from the data-src on each button
    
    var $videoSrc;  
    $('.video-container').click(function() {
        $videoSrc = $(this).data( "src" );
    });
    console.log($videoSrc);
    
      
      
    // when the modal is opened autoplay it  
    $('#modalVideo').on('shown.bs.modal', function (e) {
        
    // set the video src to autoplay and not to show related video. Youtube related video is like a box of chocolates... you never know what you're gonna get
    $("#video").attr('src',$videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
    
    })
      
    
    
    // stop playing the youtube video when I close the modal
    $('#modalVideo').on('hide.bs.modal', function (e) {
        // a poor man's stop video
        $("#video").attr('src',$videoSrc); 
    });

    // document ready
    $(".header-menu-button").click(function(){
        if ($(this).hasClass("header-menu-button-close")){
            $(this).removeClass("header-menu-button-close");
            $(this).children(".hamburger").removeClass("active");
            $(".header-menu-mobile").css({"height":"80px","box-shadow": "rgba(0, 0, 0, 0) 0px 30px 60px -10px"});
            $(".mobile-nav-container").css("opacity","0");
        }
        else
        {
            $(this).addClass("header-menu-button-close");
            $(this).children(".hamburger").addClass("active");
            $(".header-menu-mobile").css({"height":"564px","box-shadow": "rgba(0, 0, 0, 0.2) 0px 30px 60px -10px"});
            $(".mobile-nav-container").css("opacity","1");
        }
    });
});
