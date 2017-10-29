
function init() {
    var canvas = {}
    canvas.element = document.getElementById("mainCanvas")
    canvas = initializeCanvas(canvas);
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
        canvas.ctx.moveTo(canvas.x, canvas.y);
        canvas.ctx.lineTo(e.x, e.y);
        canvas.ctx.stroke();
        //TODO:
        //Send update to server here
        //**************************
        canvas.x = e.x;
        canvas.y = e.y;
    }

    canvas.element.onmouseleave = function(e) {
        canvas.isDrawing = false;
    }
    return canvas;
}


function initializeStyle(canvas) {
    canvas.setAttribute('width', document.body.clientWidth * .8 + 'px');
    canvas.setAttribute('height', document.body.clientHeight * .8 + 'px');
    canvas.style.borderStyle = 'solid';
    canvas.style.borderWidth = '3px';
    canvas.style.borderColor = 'black';
    canvas.isDrawing = true;
    return canvas;
}
