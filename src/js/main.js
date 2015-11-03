//using Mary Rose Cook and RainingChain's tutorial videos as my two biggest references/resources
;(function() { //IIFE

  var Game = function(canvasId) { //holds all the main game code
    var canvas = document.getElementById(canvasId); //get the canvas into my game
    var screen = canvas.getContext('2d'); //var screen will allow me to draw to the canvas. "2d" leads to the creation of a CanvasRenderingContext2D object representing a two-dimensional rendering context.
    var gameSize = { x: canvas.width, y: canvas.height }; // stores the width and height of the canvas for later use for placing entities on the canvas

    this.bodies = [new Player(this, gameSize)]; //will hold all of the bodies in the game

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
        drawDrillHead(screen, this.bodies[i]);
      }
    }
  };

  var Player = function(game, gameSize) {
    this.game = game;
    this.size = { x: 16, y: 16 }; //player size
    this.center = { x: gameSize.x / 2, y: gameSize.y - this.size.x};//tells the game where the player is at the moment, starting at half way through the screen and just above the bottom
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
        }  else {
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

  var drawTank = function(screen, body) {
    //tank body
    screen.fillRect(body.center.x - body.size.x / 2, //x coordinate
                    body.center.y - body.size.y / 2, // y coordinate
                    body.size.x, body.size.y); //width and hieght

    //drill head
    // screen.fillRect(body.center.x - body.size.x / 2,
    //                 body.center.y - body.size.y / 2,
    //                 body.size.x, body.size.y);
  };

  var drawDrillHead = function(screen, body) {
    screen.fillRect(body.center.x - 1, body.center.y - body.size.y/2 - 5, 4, 5);
  };

  var Keyboarder = function() { //handles keyboard input
    var keyState= {}; //records if any key that's been pressed is pressed or released

    window.onkeydown = function(e) {
      keyState[e.keyCode] = true;
    };

    window.onkeyup = function(e) {
      keyState[e.keyCode] = false;
    };

    this.isDown = function(keyCode) {
      return keyState[keyCode] === true;
    };

    this.KEYS = { LEFT: 37, UP: 38, RIGHT: 39, DOWN: 40, SPACE: 32};
  };

  window.onload = function() { //instantiate the game once the DOM is ready with the canvas
    new Game("screen"); //pass in the id of the canvas I want to write into
  };
})(); // End of IIFE
