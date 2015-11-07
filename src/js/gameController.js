(function() { //IIFE

    var DJANGO_SERVER_URL = "https://cryptic-citadel-5628.herokuapp.com/api";
    var FIREBASE_SERVER_URL = "https://tanks-for-waiting.firebaseio.com";

    angular.module('tanks-for-waiting').controller('GameController', GameController);
    GameController.$inject = ['$scope', '$http', '$firebaseObject'];

    function GameController($scope, $http, $firebaseObject) {

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
                    playerID = response.data;
                    //this is where I would display the tutorial
                    $http.post(DJANGO_SERVER_URL + "/game/" + playerID)
                        .then(function(response) {
                                gameID = response.data;
                                firebaseref = new Firebase (FIREBASE_SERVER_URL + "/games/" + gameID); //websocket to firebase api
                                $scope.game = $firsebaseObject (firebaseref); //websocket to firebase api
                                // $scope.gameRunning = true;
                                // new Game("screen");
                            },
                            function(errobj) {
                                alert("Game request failed: " + JSON.stringify(errobj));
                            });
                }, function(errobj) {
                  $scope.gameRunning = true;
                  new Game("screen");
                    // alert("Player request failed: " + JSON.stringify(errobj));
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

            this.bodies = [new Player(this, gameSize)]; //will hold all of the bodies in the game
            this.targets = [new Target(this, gameSize),
                new Target(this, gameSize),
                new Target(this, gameSize),
                new Target(this, gameSize),
                new Target(this, gameSize)
            ];
            var self = this;
            var framesPerSecond = function() { // framesPerSecond is going to get run about 60 times a second and it's responsible for running all the main game logic
                self.update(); //updates the screen
                self.draw(screen, gameSize); //based upon what's happening in the game
                requestAnimationFrame(framesPerSecond); // and then asks to run framesPerSecond again
                // console.log("hello"); // uncomment the console log to see this 60fps in action
            };

            framesPerSecond();

        };

        Game.prototype = { //gives Game a prototype
            update: function() { //updates the movement of all the on screen entities
                for (var i = 0; i < this.bodies.length; i++) {
                    this.bodies[i].update();
                }
            },

            draw: function(screen, gameSize) {
                screen.clearRect(0, 0, gameSize.x, gameSize.y);
                for (var i = 0; i < this.bodies.length; i++) {
                    drawTank(screen, this.bodies[i]);
                    // drawTarget(screen, this.bodies[i]);
                    if (i === 0) {
                        if (this.bodies[i].keyboarder.isDown(this.bodies[i].keyboarder.KEYS.LEFT)) {
                            drawDrillHeadLeft(screen, this.bodies[i]);
                        } else if (this.bodies[i].keyboarder.isDown(this.bodies[i].keyboarder.KEYS.RIGHT)) {
                            drawDrillHeadRight(screen, this.bodies[i]);
                        } else if (this.bodies[i].keyboarder.isDown(this.bodies[i].keyboarder.KEYS.UP)) {
                            drawDrillHeadUp(screen, this.bodies[i]);
                        } else if (this.bodies[i].keyboarder.isDown(this.bodies[i].keyboarder.KEYS.DOWN)) {
                            drawDrillHeadDown(screen, this.bodies[i]);
                        }
                    }
                }
                for (i = 0; i < this.targets.length; i++) {
                    drawTarget(screen, this.targets[i]);
                    // drawTarget(screen, this.bodies[i]);

                }
            },

            addBody: function(body) { //takes a body and pushes it to the bodies array
                this.bodies.push(body); // example; this.game.addBody(varNameOfBody);
            }
        };
        var Player = function(game, gameSize) {
            this.game = game;
            this.size = {
                x: 16,
                y: 16
            }; //player size
            this.center = {
                x: gameSize.x / 2,
                y: gameSize.y - this.size.x
            }; //tells the game where the player is at the moment, starting at half way through the screen and just above the bottom
            this.keyboarder = new Keyboarder();
        };

        Player.prototype = {
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

        var Target = function(game, gameSize) {
            this.game = game;
            this.size = {
                x: 10,
                y: 10
            }; //player size
            this.center = {
                x: Math.random() * gameSize.x,
                y: Math.random() * gameSize.y
            }; //tells the game where the player is at the moment, starting at half way through the screen and just above the bottom
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
    }
})(); // End of IIFE
