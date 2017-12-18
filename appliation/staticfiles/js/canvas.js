var canvas = {}

function init() {
    //initializes canvas
    canvas.element = document.getElementById("mainCanvas")
    canvas = initializeCanvas(canvas);
}

function initializeCanvas(canvas) {
    canvas.element = initializeStyle(canvas.element);
    canvas.isDrawing = false;
    canvas.ctx = canvas.element.getContext('2d');

    //updates mouse position
    canvas.element.onmousedown = function(e) {
        if (canvas.isDrawing) {
            return;
        }
        canvas.x = e.x;
        canvas.y = e.y;
        canvas.isDrawing = true;
    }

    //ceases drawing
    canvas.element.onmouseup = function(e) {
        canvas.isDrawing = false;
    }

    //fills in white circles as mouse moves
    canvas.element.onmousemove = function(e) {
        if (!canvas.isDrawing) {
            return;
        }
        canvas.ctx.beginPath();
        canvas.ctx.fillStyle = 'white';
        canvas.ctx.arc(e.x, e.y, 15, 0, 2 * Math.PI, false);

        //fills in circles between two points detected by the canvas
        //for smoother appearance
        var grain = 10;
        var xDiff = (canvas.x - e.x)/grain;
        var yDiff = (canvas.y - e.y)/grain;
        for (var i = 0; i < grain; i++) {
            canvas.ctx.arc(e.x + i * xDiff, e.y + i * yDiff, 15, 0, 2 * Math.PI, false);
        }

        //draws relevant points and updates position
        canvas.ctx.fill();
        canvas.x = e.x;
        canvas.y = e.y;
    }

    canvas.element.onmouseleave = function(e) {
        canvas.isDrawing = false;
    }
    return canvas;
}

function initializeStyle(canvas) {
    // canvas context
    canvas.ctx = canvas.getContext("2d");

    // makes a square canvas
    canvas.setAttribute('width', document.body.clientHeight * .8 + 'px');
    canvas.setAttribute('height', document.body.clientHeight * .8 + 'px');

    //initializes all other canvas attributes
    canvas.style.borderStyle = 'solid';
    canvas.style.borderWidth = '3px';
    canvas.style.borderColor = 'black';
    canvas.ctx.fillStyle = "black";
    canvas.ctx.fillRect(0, 0, canvas.width, canvas.height);
    canvas.isDrawing = true;
    return canvas;
}

function classify() {
    //get image data
    var image = canvas.element.getContext('2d').getImageData(
        0,
        0,
        canvas.element.width,
        canvas.element.height
    );
    //send data to classifier as POST request
    var request = new XMLHttpRequest();
    request.open('POST', 'http://127.0.0.1:8000/classify', true);
    request.send(image.data);

    //waits 200ms before refreshing
    //Better way to do update would be ajax, not page reload
    setTimeout(
        function() {location.reload(true);},
        200
    );
}
