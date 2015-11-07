(function() { //IIFE
    var DJANGO_SERVER_URL = "abc";
    angular.module('tanks-for-waiting').controller('GameController', GameController);
    GameController.$inject = ['$scope', '$http'];

    function GameController($scope, $http) {
        $scope.gameNotRunning = true;
        $scope.score = 0;
        $scope.startGame = function() {
            $http.post(DJANGO_SERVER_URL + "/players/")
                .then(function() {
                    $scope.gameNotRunning = false;
                }, function(errobj) {
                    alert("Game request failed: " + JSON.stringify(errobj));
                });
            console.log("click");
        };
    }
})(); // End of IIFE
