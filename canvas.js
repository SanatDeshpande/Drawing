
function init() {
    var canvas = {}
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
