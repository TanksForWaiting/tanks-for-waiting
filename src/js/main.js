;(function() { //IIFE

  var Game = function(canvasId) { //holds all the main game code
    var canvas = document.getElementById(canvasId); //get the canvas into my game
    var screen = canvas.getContext('2d'); //var screen will allow me to draw to the canvas. "2d" leads to the creation of a CanvasRenderingContext2D object representing a two-dimensional rendering context.
    var gameSize = { x: canvas.width, y: canvas.height }; // stores the width and height of the canvas for later use for placing entities on the canvas

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
      screen.fillRect(30, 30, 40, 40);
    }
  };

  window.onload = function() { //instantiate the game once the DOM is ready with the canvas
    new Game("screen"); //pass in the id of the canvas I want to write into
  };
})(); // End of IIFE
