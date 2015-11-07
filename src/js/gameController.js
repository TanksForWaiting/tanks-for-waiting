(function() { //IIFE
    var DJANGO_SERVER_URL = "abc";
    angular.module('tanks-for-waiting').controller('GameController', GameController);
    GameController.$inject = ['$scope', '$http'];

    function GameController($scope, $http) {
        var playerID = null; //player_id stored here
        var gameID = null; //game_id stored here
        $scope.gameRunning = false;
        $scope.score = 0;
        $scope.startGame = function() {
            $http.post(DJANGO_SERVER_URL + "/players/")
                .then(function(response) {
                    playerID = response.data;
                    //this is where I would display the tutorial
                    $http.post(DJANGO_SERVER_URL + "/game/" + playerID)
                        .then(function(response) {
                                gameID = response.data;
                                $scope.gameRunning = true;
                            },
                            function(errobj) {
                              alert("Game request failed: " + JSON.stringify(errobj));
                            });
                }, function(errobj) {
                    alert("Player request failed: " + JSON.stringify(errobj));
                });
            console.log("click");
        };
    }
})(); // End of IIFE
