(function() { //IIFE

    var DJANGO_SERVER_URL = "https://cryptic-citadel-5628.herokuapp.com/api";
    var FIREBASE_SERVER_URL = "https://tanks-for-waiting.firebaseio.com";

    angular.module('tanks-for-waiting').controller('GameController', GameController);
    GameController.$inject = ['$scope', '$http', '$interval', '$firebaseObject'];

    function GameController($scope, $http, $interval, $firebaseObject) {

        var firebaseref = null;
        var playerID = null; //player_id stored here
        var gameID = null; //game_id stored here
        $scope.gameRunning = false;
        $scope.score = 0;
        /*
        *This begins the process of game selection.
        POST to /players/ for player_id
        Returns player_id
        Stores player_id
        POST to games/player_id
        Returns game_id
        Stores game_id
        Starts game
        */
        $scope.startGame = function() {
            $http.post(DJANGO_SERVER_URL + "/players/")
                .then(function(response) {
                    playerID = response.data.player_id;
                    //this is where I would display the tutorial
                    $http.post(DJANGO_SERVER_URL + "/games/", {
                            player_id: playerID
                        })
                        .then(function(response) {
                                gameID = response.data.game_id;
                                firebaseref = new Firebase(FIREBASE_SERVER_URL + "/games/" + gameID); //websocket to firebase api
                                var obj = $firebaseObject(firebaseref); //websocket to firebase api
                                obj.$bindTo($scope, "game").then(function() {
                                    console.log($scope.game); // { foo: "bar" }
                                    $scope.gameRunning = true;
                                    new Game("screen");
                                });
                            },
                            function(errobj) {
                                alert("Game request failed: " + JSON.stringify(errobj, null, 2));
                            });
                }, function(errobj) {
                    // $scope.gameRunning = true;
                    // new Game("screen");
                    alert("Player request failed: " + JSON.stringify(errobj));
                });
            console.log("click");
        };

        var Game = function(canvasId) { //holds all the main game code
            var canvas = document.getElementById(canvasId); //get the canvas into my game
            var screen = canvas.getContext('2d'); //var screen will allow me to draw to the canvas. "2d" leads to the creation of a CanvasRenderingContext2D object representing a two-dimensional rendering context.
            var gameSize = {
                x: canvas.width,
                y: canvas.height
            }; // stores the width and height of the canvas for later use for placing entities on the canvas

            var self = this;

            this.tanks = [new Player(this, $scope.game.tanks[playerID])]; //will hold all of the tanks in the game
            this.tanks.concat(self.refreshTanks(this));
            this.targets = self.refreshTargets(this);

            $interval(function() {
              if (self.isReady) {
                self.update(); //updates the screen
                self.draw(screen, gameSize); //based upon what's happening in the game
              }
            }, 16.7);
        };

        Game.prototype = { //gives Game a prototype

            isReady: true,

            update: function() { //updates the movement of all the on screen entities
                for (var i = 0; i < this.tanks.length; i++) {
                    this.tanks[i].update();
                }

                var thisPlayer = this.tanks[0];

                for (i = 0; i < this.targets.length; i++) {
                    if (colliding(thisPlayer, this.targets[i])) {
                        this.isReady = false;
                        $scope.game.tanks[playerID].x = thisPlayer.location().x;
                        $scope.game.tanks[playerID].y = thisPlayer.location().y;
                        console.log("HIT!");

                        postDjango(targetHit).then(function(response) {
                          if (response.nope) {
                            // Did not hit target.

                          } else {
                            // Was a hit.
                            // Update score from $scope.game.tanks[playID];
                          }
                          this.isReady = true;
                        }, function(errobj) {
                          // Post failed!
                        });

                        // $scope.score += 1;
                        // this.targets.splice(i, 1);
                    }
                }
                this.tanks = this.tanks.slice(0,1).concat(this.refreshTanks(this));
                this.targets = this.refreshTargets(this);
            },

            draw: function(screen, gameSize) {
                screen.clearRect(0, 0, gameSize.x, gameSize.y);
                for (var i = 0; i < this.tanks.length; i++) {
                    drawTank(screen, this.tanks[i]);
                    // drawTarget(screen, this.tanks[i]);
                    if (i === 0) {
                        if (this.tanks[i].keyboarder.isDown(this.tanks[i].keyboarder.KEYS.LEFT)) {
                            drawDrillHeadLeft(screen, this.tanks[i]);
                        } else if (this.tanks[i].keyboarder.isDown(this.tanks[i].keyboarder.KEYS.RIGHT)) {
                            drawDrillHeadRight(screen, this.tanks[i]);
                        } else if (this.tanks[i].keyboarder.isDown(this.tanks[i].keyboarder.KEYS.UP)) {
                            drawDrillHeadUp(screen, this.tanks[i]);
                        } else if (this.tanks[i].keyboarder.isDown(this.tanks[i].keyboarder.KEYS.DOWN)) {
                            drawDrillHeadDown(screen, this.tanks[i]);
                        }
                    }
                }
                for (i = 0; i < this.targets.length; i++) {
                    drawTarget(screen, this.targets[i]);
                    // drawTarget(screen, this.tanks[i]);

                }
            },

            refreshTanks: function(thisGame) {
              var tanks = [];
                for (var key in $scope.game.tanks) {
                    if (key !== playerID) {
                        tanks.push(new Player(this, $scope.game.tanks[key]));
                    }
                }
                return tanks;
            },

            refreshTargets: function(thisGame) {
                var targets = [];
                for (var key in $scope.game.targets) {
                    targets.push(new Target(thisGame, $scope.game.targets[key]));
                }
                return targets;
            }
        };
        var Player = function(game, location) {
            this.game = game;
            this.size = {
                x: 16,
                y: 16
            }; //player size
            this.center = {
                x: location.x,
                y: location.y
            }; //tells the game where the player is at the start
            this.keyboarder = new Keyboarder();
        };

        Player.prototype = {

            location: function() {
              return this.center;
            },

            update: function() {
                if (this.keyboarder.isDown(this.keyboarder.KEYS.LEFT)) {
                    if (this.center.x <= 10) {
                        this.center.x = 8;
                    } else {
                        this.center.x -= 2;
                    }
                }
                if (this.keyboarder.isDown(this.keyboarder.KEYS.RIGHT)) {
                    if (this.center.x >= 490) {
                        this.center.x = 492;
                    } else {
                        this.center.x += 2;
                    }
                }
                if (this.keyboarder.isDown(this.keyboarder.KEYS.UP)) {
                    if (this.center.y <= 10) {
                        this.center.y = 8;
                    } else {
                        this.center.y -= 2;
                    }
                }
                if (this.keyboarder.isDown(this.keyboarder.KEYS.DOWN)) {
                    if (this.center.y >= 490) {
                        this.center.y = 492;
                    } else {
                        this.center.y += 2;
                    }
                }
            }
        };

        var Target = function(game, location) {
            this.game = game;
            this.size = {
                x: 10,
                y: 10
            }; //player size
            this.center = {
                x: location.x,
                y: location.y
            }; //tells the game where the targets are at the moment, starting at half way through the screen and just above the bottom
        };

        Target.prototype = {
            update: function() {
                console.log("helllo");
            }
        };

        var drawTank = function(screen, body) {
            //tank body
            screen.fillRect(body.center.x - body.size.x / 2, //x coordinate
                body.center.y - body.size.y / 2, // y coordinate
                body.size.x, body.size.y); //width and hieght
        };

        var drawDrillHeadLeft = function(screen, body) {
            screen.fillRect(body.center.x - body.size.x / 2 - 4, body.center.y - 2, 4, 4);
        };

        var drawDrillHeadRight = function(screen, body) {
            screen.fillRect(body.center.x + body.size.x / 2, body.center.y - 2, 4, 4);
        };

        var drawDrillHeadUp = function(screen, body) {
            screen.fillRect(body.center.x - 2, body.center.y - body.size.y / 2 - 4, 4, 4);
        };

        var drawDrillHeadDown = function(screen, body) {
            screen.fillRect(body.center.x - 2, body.center.y + body.size.y / 2, 4, 4);
        };

        var drawTarget = function(screen, target) {
            screen.fillRect(target.center.x - target.size.x / 2, //x coordinate
                target.center.y - target.size.y / 2, // y coordinate
                target.size.x, target.size.y);
        };

        var Keyboarder = function() { //handles keyboard input
            var keyState = {}; //records if any key that's been pressed is pressed or released

            window.onkeydown = function(e) {
                keyState[e.keyCode] = true;
            };

            window.onkeyup = function(e) {
                keyState[e.keyCode] = false;
            };

            this.isDown = function(keyCode) {
                return keyState[keyCode] === true;
            };

            this.KEYS = {
                LEFT: 37,
                UP: 38,
                RIGHT: 39,
                DOWN: 40,
                SPACE: 32
            };
        };

        var colliding = function(b1, b2) {
            return !(b1 === b2 ||
                b1.center.x + b1.size.x / 2 < b2.center.x - b2.size.x / 2 ||
                b1.center.y + b1.size.y / 2 < b2.center.y - b2.size.y / 2 ||
                b1.center.x - b1.size.x / 2 > b2.center.x + b2.size.x / 2 ||
                b1.center.y - b1.size.y / 2 > b2.center.y + b2.size.y / 2);
        };
    }
})(); // End of IIFE
