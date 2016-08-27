# IceCTF 2016
## Solution By: Nullp0inter

# Spotlight Web 10pts
Someone turned out the lights and now we can't find anything. Send halp! spotlight

# Solution:
Obviously with around 1600 solves, not a lot of people need this but in case you do I figured I would include it for completeness' sake.
The challenge sends you to spotlight.vuln.icec.tf, a mostly black page with a white circle that is supposed to be your "spotlight." If you
take a few minutes to search around you'll see some messages such as "not here", "the flag is close", etc. But we couldn't find the flag.
So what do we do then? Well it's usually idea to "USE THE SOURCE, LUKE!." In Firefox you can easily do this with ctrl+U. The source is fairly
small so I will post it here:

```html
<!DOCTYPE html>
<html>
    <head>
        <title>IceCTF 2016 - Spotlight</title>
        <link rel="stylesheet" type="text/css" href="spotlight.css">
    </head>
    <body>
        <!-- Hmmm... not here either? -->

        <canvas id="myCanvas" style="background-color:#222;">
            Your browser does not support the HTML5 canvas tag.
        </canvas>
        <script src="spotlight.js"></script>
    </body>
</html>
```

So two things should pop out at you, the `spotlight.css` and the `spotlight.js` at the bottom. The css is just unlikely so I ignored that altogether
and went straight for the javascript file as that is what is making the spotlight on the page work in the first place and holds the messages. We click
on the `spotlight.js` to view the source for that and get:

```javascript
/*
 * TODO: Remove debug log
 */

// Load the canvas context
console.log("DEBUG: Loading canvas context...");
var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');

// Make the canvas fill the screen
console.log("DEBUG: Adjusting canvas size...");
context.canvas.width  = window.innerWidth;
context.canvas.height = window.innerHeight;

// Mouse listener
console.log("DEBUG: Adding mouse listener...");
canvas.addEventListener('mousemove', function(evt) {
    spotlight(canvas, getMousePos(canvas, evt));
}, false);

console.log("DEBUG: Initializing spotlight sequence...");
function spotlight(canvas, coord) {
    // Load up the context
    var context = canvas.getContext('2d');

    // Clear the canvas
    context.clearRect(0,0,canvas.width, canvas.height);

    // Turn off the lights! Mwuhahaha >:3
    context.fillRect(0,0,window.innerWidth,window.innerHeight);

    // Scatter around red herrings
    context.font = "20px Arial";
    context.fillText("Not here.",width(45),height(60));
    context.fillText("Keep looking...",width(80),height(20));
    context.fillText(":c",width(20),height(30));
    context.fillText("Look closer!",width(75),height(80));
    context.fillText("Almost there!",width(60),height(10));
    context.fillText("Howdy!",width(10),height(90));
    context.fillText("Closer...",width(30),height(80));
    context.fillText("FLAG AHOY!!!!!!!!1",width(80),height(95));

    // Turn on the flash light
    var grd = context.createRadialGradient(
        coord.x, coord.y,  75,
        coord.x, coord.y,  50);
    grd.addColorStop(0,'rgba(255,255,255,0)');
    grd.addColorStop(1,'rgba(255,255,255,.7)');

    context.fillStyle=grd;
}

console.log("DEBUG: IceCTF{5tup1d_d3v5_w1th_th31r_l095}");

console.log("DEBUG: Loading up helper functions...");
console.log("DEBUG:     * getMousePos(canvas, evt)");
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x:  evt.clientX - rect.left,
        y:  evt.clientY - rect.top
    };
}

// Calculate height percenteges
console.log("DEBUG:     * height(perc)");
function height(perc)
{
    var h = window.innerHeight;
    return h * (perc / 100);
}

// Calculate width percenteges
console.log("DEBUG:     * width(perc)");
function width(perc)
{
    var w = window.innerWidth;
    return w * (perc / 100);
}
console.log("DEBUG: Done.");

console.log("DEBUG: Ready for blast off!");
```

Well what do you know, about halfway down we can see our flag:
`IceCTF{5tup1d_d3v5_w1th_th31r_l095}`
