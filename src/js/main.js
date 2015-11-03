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
    update: function() {

    },

    draw: function(screen, gameSize) {
      for (var i = 0; i < this.bodies.length; i++) {
        drawRect(screen, this.bodies[i]);
      //first number is the x, the second the y and the final two are the width and height
      }
    }
  };

  var Player = function(game, gameSize) {
    this.game = game;
    this.size = { x: 15, y: 15 }; //player size
    this.center = { x: gameSize.x / 2, y: gameSize.y - this.size.x};//tells the game where the player is at the moment, starting at half way through the screen and just above the bottom
  };

  Player.prototype = {
    update: function() {

    }
  };

  var drawRect = function(screen, body) {
    screen.fillRect(body.center.x - body.size.x / 2, //x coordinate
                    body.center.y - body.size.y / 2, // y coordinate
                    body.size.x, body.size.y); //width and hieght
  };

  window.onload = function() { //instantiate the game once the DOM is ready with the canvas
    new Game("screen"); //pass in the id of the canvas I want to write into
  };
})(); // End of IIFE
