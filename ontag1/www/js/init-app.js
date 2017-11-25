initEvents = function () {
    var el, evt ;

    if (navigator.msPointerEnabled || !('ontouchend' in window))    // if on Win 8 machine or no touch
        evt = "click" ;                                             // let touch become a click event
    else                                                            // else, assume touch events available
        evt = "touchend" ;                                          // not optimum, but works
} ;
document.addEventListener("deviceready",initEvents, false) ;