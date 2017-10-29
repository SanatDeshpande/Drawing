
function init() {
    var canvas = {}
    canvas.element = document.getElementById("mainCanvas")
    canvas = initializeCanvas(canvas);
}

function initializeCanvas(canvas) {
    canvas.element = initializeStyle(canvas.element);

    canvas.ctx = canvas.element.getContext('2d');

    canvas.element.onmousedown = function(e) {
        console.log(e.x, e.y);
    }

    return canvas;
}

function initializeStyle(canvas) {
    canvas.style.width = '80%';
    canvas.style.height = '80%';
    canvas.style.borderStyle = 'solid';
    canvas.style.borderWidth = '3px';
    canvas.style.borderColor = 'black';
    canvas.isDrawing = true;
    return canvas;
}
