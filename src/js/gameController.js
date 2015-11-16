(function() { //IIFE

    var DJANGO_SERVER_URL = "https://cryptic-citadel-5628.herokuapp.com/api";
    var FIREBASE_SERVER_URL = "https://tanks-for-waiting.firebaseio.com";

    angular.module('tanks-for-waiting').controller('GameController', GameController);
    GameController.$inject = ['$scope', '$http', '$interval', '$firebaseObject', '$firebaseArray'];

    function GameController($scope, $http, $interval, $firebaseObject, $firebaseArray) {

        var firebasePlayerRef = null;
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
                                firebasePlayerRef = new Firebase(FIREBASE_SERVER_URL + "/games/" + gameID + "/tanks/" + playerID); //websocket to firebase api
                                var playerObj = $firebaseObject(firebasePlayerRef); //websocket to firebase api
                                playerObj.$bindTo($scope, "player").then(function() {
                                    console.log($scope.player); // { foo: "bar" }
                                    new Game("screen");
                                });
                                firebaseScoreRef = new Firebase(FIREBASE_SERVER_URL + "/games/" + gameID + "/scores/" + playerID);
                                var scoreObj = $firebaseObject(firebaseScoreRef);
                                scoreObj.$bindTo($scope, "score").then(function() {
                                    console.log($scope.score); // { foo: "bar" }
                                    // new Game("screen");
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
            //initalizing the targets
            firebaseTargetsRef = new Firebase(FIREBASE_SERVER_URL + "/games/" + gameID + "/targets/");
            var targetsObj = $firebaseObject(firebaseTargetsRef);
            $firebaseArray(firebaseTargetsRef).$loaded()
                .then(function(targets) {
                    self.targets = self.refreshTargets(this, targets);
                    $scope.gameRunning = true;
                    $interval(function() {
                        if (self.isReady) {
                            self.update(); //updates the screen
                            self.draw(screen, gameSize); //based upon what's happening in the game
                        }
                    }, 16.7);
                }, function() {
                    console.log("Failed to load targets");
                });

            var targetAdded = function() {
                if ($scope.gameRunning) {
                    console.log("it was hit");
                    $firebaseArray(firebaseTargetsRef).$loaded()
                        .then(function(targets) {
                            self.targets = self.refreshTargets(this, targets);
                        });
                }

            };
            var targetRemoved = function(dataSnapshot) {
                var destroyedTarget = dataSnapshot.val();
                //draw explosion at x/y location ( destroyedTarget.x, destroyedTarget.y )
                // new Explosion(location, duration)
            };

            firebaseTargetsRef.on("child_added", targetAdded,
                function(err) {
                    console.log("failed");
                });
            firebaseTargetsRef.on("child_removed", targetRemoved,
                function(err) {
                    console.log("failed");
                });

            this.tanks = [new Player(this, $scope.player)]; //will hold all of the tanks in the game
            // this.tanks.concat(self.refreshTanks(this));
            this.walls = [
                // left outter wall
                new Wall(this, 40, 40, 45, 460),
                new Wall(this, 40, 40, 225, 45),
                new Wall(this, 40, 460, 225, 455),
                //right outer wall
                new Wall(this, 275, 40, 460, 45),
                new Wall(this, 460, 40, 455, 460),
                new Wall(this, 275, 455, 455, 460),
                //top center wall
                new Wall(this, 80, 80, 420, 85),
                new Wall(this, 80, 80, 85, 225),
                new Wall(this, 415, 80, 420, 225),
                //bottom center wall
                new Wall(this, 80, 275, 85, 420),
                new Wall(this, 85, 415, 420, 420),
                new Wall(this, 415, 275, 420, 420),
                //left center wall
                new Wall(this, 225, 145, 230, 350),
                new Wall(this, 120, 250, 225, 255),
                //right center wall
                new Wall(this, 275, 145, 280, 350),
                new Wall(this, 275, 250, 380, 255)
            ];
        };

        Game.prototype = { //gives Game a prototype

            isReady: true,

            update: function() { //updates the movement of all the on screen entities
                for (var i = 0; i < this.tanks.length; i++) {
                    this.tanks[i].update();
                }

                var thisPlayer = this.tanks[0];

                var deleteError = function(errobj) {
                    console.log('Error deleting target: ' + JSON.stringify(errobj));
                };

                var deleteSuccess = function(response) {
                    console.log(response);
                    if (response.nope) {
                        // Did not hit target.
                        //if no, return something (currently it returns the string “nope” but that can be changed)
                    } else {
                        // Was a hit.
                        // Update score from $scope.game.tanks[playID];
                    }
                };
                $scope.player.x = thisPlayer.location().x;
                $scope.player.y = thisPlayer.location().y;
                $scope.player.direction = thisPlayer.direction;

                for (i = 0; i < this.targets.length; i++) {
                    if (collidingTarget(thisPlayer, this.targets[i])) {
                        // this.isReady = false;
                        this.targets[i].fillStyle = 'black';
                        console.log(this.targets[i].target_id);
                        if (this.targets[i].is_hit === 0) {
                            // console.log("HIT!");
                            console.log(playerID);
                            this.targets[i].is_hit = 1;
                            $http.delete(DJANGO_SERVER_URL + "/games/" + gameID + "/targets/" + this.targets[i].target_id + "/", {

                                data: playerID

                            }).then(deleteSuccess, deleteError);

                        }
                        // this.isReady = true;
                        // $scope.score += 1;
                        // this.targets.splice(i, 1);
                    }
                }
                this.tanks = this.tanks.slice(0, 1); //.concat(this.refreshTanks(this)); --add back in for multiplayer
                // this.targets = this.refreshTargets(this);
            },

            draw: function(screen, gameSize) {
                screen.clearRect(0, 0, gameSize.x, gameSize.y);

                for (i = 0; i < this.targets.length; i++) { //This loop draws the targets
                    drawTarget(screen, this.targets[i]);
                }

                for (i = 0; i < this.walls.length; i++) { //This loop draws the walls
                    this.walls[i].draw(screen);
                }

                for (var i = 0; i < this.tanks.length; i++) { //This loop draws the tanks
                    drawTank(screen, this.tanks[i]);
                    if (i === 0) {
                        if (this.tanks[i].direction === "W") {
                            drawDrillHeadLeft(screen, this.tanks[i]);
                        } else if (this.tanks[i].direction === "E") {
                            drawDrillHeadRight(screen, this.tanks[i]);
                        } else if (this.tanks[i].direction === "N") {
                            drawDrillHeadUp(screen, this.tanks[i]);
                        } else if (this.tanks[i].direction === "S") {
                            drawDrillHeadDown(screen, this.tanks[i]);
                        }
                    }
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

            refreshTargets: function(thisGame, firebaseTargets) {
                var targets = [];
                for (var i = 0; i < firebaseTargets.length; i++) {
                    targets.push(new Target(thisGame, firebaseTargets[i]));
                }
                return targets;
            }
        };
        var Player = function(game, location) {
            this.game = game;
            this.direction = "E";
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
                var wallHit = false;
                for (i = 0; i < this.game.walls.length; i++) {
                    if (collidingWall(this, this.game.walls[i])) {
                        console.log("Wall!");
                        wallHit = true;
                        break;
                    }
                }

                if (this.keyboarder.isDown(this.keyboarder.KEYS.LEFT)) {
                    this.direction = "W";
                    if (wallHit) {
                        this.center.x += 8;
                    } else if (this.center.x <= 10) {
                        this.center.x = 8;
                    } else {
                        this.center.x -= 2;
                    }
                } else if (this.keyboarder.isDown(this.keyboarder.KEYS.RIGHT)) {
                    this.direction = "E";
                    if (wallHit) {
                        this.center.x -= 8;
                    } else if (this.center.x >= 490) {
                        this.center.x = 492;
                    } else {
                        this.center.x += 2;
                    }
                } else if (this.keyboarder.isDown(this.keyboarder.KEYS.UP)) {
                    this.direction = "N";

                    if (wallHit) {
                        this.center.y += 8;
                    } else if (this.center.y <= 10) {
                        this.center.y = 8;
                    } else {
                        this.center.y -= 2;
                    }
                } else if (this.keyboarder.isDown(this.keyboarder.KEYS.DOWN)) {
                    this.direction = "S";

                    if (wallHit) {
                        this.center.y -= 8;
                    } else if (this.center.y >= 490) {
                        this.center.y = 492;
                    } else {
                        this.center.y += 2;
                    }
                }
            }
        };

        var Target = function(game, firebaseTarget) {
            this.game = game;
            this.size = {
                x: 10,
                y: 10
            }; //player size
            this.center = {
                x: firebaseTarget.x,
                y: firebaseTarget.y
            }; //tells the game where the targets are at the moment, starting at half way through the screen and just above the bottom
            this.target_id = firebaseTarget.$id;
            this.is_hit = 0;
            this.fillStyle = "red";
        };

        Target.prototype = {
            update: function() {
                console.log("helllo");
            }
        };

        var Wall = function(game, xmin, ymin, xmax, ymax) {
            this.game = game;
            this.xmin = xmin;
            this.ymin = ymin;
            this.xmax = xmax;
            this.ymax = ymax;
        };

        Wall.prototype = {
            draw: function(screen) {
                screen.fillStyle = 'white';
                screen.fillRect(this.xmin, //x coordinate
                    this.ymin, // y coordinate
                    this.xmax - this.xmin, //width
                    this.ymax - this.ymin); //height
            }
        };

        var drawTank = function(screen, body) {
            //tank body
            screen.fillStyle = 'green';
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
            screen.fillStyle = target.fillStyle;
            screen.fillRect(target.center.x - target.size.x / 2, //x coordinate
                target.center.y - target.size.y / 2, // y coordinate
                target.size.x, target.size.y);
        };

        var Keyboarder = function() { //handles keyboard input
            var keyState = {}; //records if any key that's been pressed is pressed or released
            var keyPressed = false;
            var self = this;

            window.onkeydown = function(e) {
                e.preventDefault();
                if (e.keyCode >= self.KEYS.LEFT &&
                    e.keyCode <= self.KEYS.DOWN &&
                    !keyPressed) {
                    keyState[e.keyCode] = true;
                    keyPressed = true;
                    e.preventDefault();
                }
            };

            window.onkeyup = function(e) {
                e.preventDefault();
                if (e.keyCode >= self.KEYS.LEFT &&
                    e.keyCode <= self.KEYS.DOWN &&
                    keyPressed) {
                    keyState = {};
                    keyPressed = false;
                }
            };

            this.isDown = function(keyCode) {
                return keyState[keyCode] === true;
            };

            this.KEYS = {
                LEFT: 37,
                UP: 38,
                RIGHT: 39,
                DOWN: 40
            };
        };

        var collidingTarget = function(b1, b2) {
            return !(b1 === b2 ||
                b1.center.x + b1.size.x / 2 < b2.center.x - b2.size.x / 2 ||
                b1.center.y + b1.size.y / 2 < b2.center.y - b2.size.y / 2 ||
                b1.center.x - b1.size.x / 2 > b2.center.x + b2.size.x / 2 ||
                b1.center.y - b1.size.y / 2 > b2.center.y + b2.size.y / 2);
        };

        var collidingWall = function(b1, b2) {
            return (((b1.center.x - b1.size.x / 2) < b2.xmax) &&
                ((b1.center.x + b1.size.x / 2) > b2.xmin) &&
                ((b1.center.y - b1.size.y / 2) < b2.ymax) &&
                ((b1.center.y + b1.size.y / 2) > b2.ymin));
            // return !(
            //     b1.center.x + b1.size.x / 2 <= b2.xmin ||
            //     b1.center.y + b1.size.y / 2 <= b2.ymax ||
            //     b1.center.x - b1.size.x / 2 >= b2.xmax ||
            //     b1.center.y - b1.size.y / 2 >= b2.ymin);
        };
    }

})(); // End of IIFE
