var canvas = {}

function init() {
    canvas.element = document.getElementById("mainCanvas")
    canvas = initializeCanvas(canvas);
    console.log("Successfully Initialized");
}

function initializeCanvas(canvas) {
    canvas.element = initializeStyle(canvas.element);
    canvas.isDrawing = false;
    canvas.ctx = canvas.element.getContext('2d');

    canvas.element.onmousedown = function(e) {
        if (canvas.isDrawing) {
            return;
        }
        canvas.x = e.x;
        canvas.y = e.y;
        canvas.isDrawing = true;
    }

    canvas.element.onmouseup = function(e) {
        canvas.isDrawing = false;
    }

    canvas.element.onmousemove = function(e) {
        if (!canvas.isDrawing) {
            return;
        }
        canvas.ctx.beginPath();
        //canvas.ctx.moveTo(canvas.x, canvas.y);
        // canvas.ctx.lineTo(e.x, e.y);
        // canvas.ctx.strokeStyle = 'white';
        // canvas.ctx.lineWidth = 10;
        canvas.ctx.fillStyle = 'white';
        canvas.ctx.arc(e.x, e.y, 15, 0, 2 * Math.PI, false);
        var grain = 10;
        var xDiff = (canvas.x - e.x)/grain;
        var yDiff = (canvas.y - e.y)/grain;
        for (var i = 0; i < grain; i++) {
            canvas.ctx.arc(e.x + i * xDiff, e.y + i * yDiff, 15, 0, 2 * Math.PI, false);
        }

        canvas.ctx.fill();
        // canvas.ctx.stroke();
        canvas.x = e.x;
        canvas.y = e.y;
    }

    canvas.element.onmouseleave = function(e) {
        canvas.isDrawing = false;
    }
    return canvas;
}


function initializeStyle(canvas) {
    canvas.ctx = canvas.getContext("2d");
    canvas.setAttribute('width', document.body.clientWidth * .8 + 'px');
    canvas.setAttribute('height', document.body.clientHeight * .8 + 'px');
    canvas.style.borderStyle = 'solid';
    canvas.style.borderWidth = '3px';
    canvas.style.borderColor = 'black';
    canvas.ctx.fillStyle = "black";
    canvas.ctx.fillRect(0, 0, canvas.width, canvas.height);
    canvas.isDrawing = true;
    return canvas;
}

function classify() {
    //downsize image
    var x = 26;
    var y = 26;
    var xStep = canvas.element.width/26;
    var yStep = canvas.element.height/26;

    var small = new Array();
    for (var i = 0; i < x; i++) {
        for (var j = 0; j < y; j++) {
            var image = canvas.element.getContext('2d').getImageData(
                i * xStep,
                j * yStep,
                i * xStep + xStep,
                j * yStep + yStep,
            );
            small.push(average(image.data));
        }
    }
    //send data to classifier as POST request
    var request = new XMLHttpRequest();
    request.open('POST', 'http://127.0.0.1:8000/classify', true);
    request.send(small);
}

function average(data) {
    var sum = 0;
    for (var i = 0; i < data.length; i+=4) {
        sum += data[i] + data[i+1] + data[i+2];
    }
    return sum/data.length;
}
