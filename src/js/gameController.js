;(function() { //IIFE
    angular.module('tanks-for-waiting')
        .controller('GameController', ['$scope', GameController]);

    function GameController($scope) {
      console.log("loaded");
    }
})(); // End of IIFE
