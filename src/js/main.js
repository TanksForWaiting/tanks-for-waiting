;(function() { //IIFE

  $('#button').click(function() {
    $('#spin-one').removeClass('tfw-hide-me');
    $('#spin-two').removeClass('tfw-hide-me');
  });

angular.module('tanks-for-waiting', ["firebase"]);

})(); // End of IIFE
