//using Mary Rose Cook and RainingChain's tutorial videos as my two biggest references/resources
;(function() { //IIFE

  $('#button').click(function() {
    $('#spin-one').removeClass('hide-me');
    $('#spin-two').removeClass('hide-me');
  });

angular.module('tanks-for-waiting', ["firebase"]);

})(); // End of IIFE
