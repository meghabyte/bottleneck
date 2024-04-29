const socket =  io('http://143.198.226.165:8000'); 
var params = new URLSearchParams(location.search);
var username = params.get('username')


window.onload = event => {
    startExperiment();
  };

var shapeType = "circle";
var color = "red";
var current_positions = [];
var current_colors = [];
var current_shape = [];
var mouse_clicked = false;
const ratio = window.devicePixelRatio;
active_canvas= document.getElementById('student-canvas-1')
active_canvas.width = 500 * ratio;
active_canvas.height = 500 * ratio;
active_canvas.style.width = "500px";
active_canvas.style.height = "500px";
active_canvas.getContext("2d").scale(ratio, ratio)
active_canvas.addEventListener('pointerdown', pointer_down, false);

function make_axis() { 
    ctx = active_canvas.getContext('2d')
    ctx.font = "15px sans-serif";
    ctx.fillStyle = "black";
    ctx.fillText("1", 485, 495);
    ctx.fillText("0", 5, 495);
    ctx.fillText("1", 3, 15);
    ctx.fillStyle = color;
}

function set_button_color(button_color) {
    if(button_color === "red") {
        document.getElementById("red-button").disabled = true;
        document.getElementById("blue-button").disabled = false;
        document.getElementById("green-button").disabled = false;
        document.getElementById("magenta-button").disabled = false;
    }
    else if(button_color === "green") {
        document.getElementById("red-button").disabled = false;
        document.getElementById("blue-button").disabled = false;
        document.getElementById("green-button").disabled = true;
        document.getElementById("magenta-button").disabled = false;
    }
    else if(button_color === "blue") {
        document.getElementById("red-button").disabled = false;
        document.getElementById("blue-button").disabled = true;
        document.getElementById("green-button").disabled = false;
        document.getElementById("magenta-button").disabled = false;
    }
    else if(button_color === "magenta") {
        document.getElementById("red-button").disabled = false;
        document.getElementById("blue-button").disabled = false;
        document.getElementById("green-button").disabled = false;
        document.getElementById("magenta-button").disabled = true;
    }
    else if(button_color === "finish") {
        document.getElementById("red-button").disabled = false;
        document.getElementById("blue-button").disabled = false;
        document.getElementById("green-button").disabled = false;
        document.getElementById("magenta-button").disabled = false;
    }
    else if(button_color === "start") {
        document.getElementById("red-button").disabled = true;
        document.getElementById("blue-button").disabled = false;
        document.getElementById("green-button").disabled = false;
        document.getElementById("magenta-button").disabled = false;
    }
    else if(button_color === "disable_all") {
        document.getElementById("red-button").disabled = true;
        document.getElementById("blue-button").disabled = true;
        document.getElementById("green-button").disabled = true;
        document.getElementById("magenta-button").disabled = true;
    }
}

function set_button_shape(button_shape) {
    if(button_shape === "circle") {
        document.getElementById("circle-button").disabled = true;
        document.getElementById("triangle-button").disabled = false;
        document.getElementById("square-button").disabled = false;
    }
    else if(button_shape === "triangle") {
        document.getElementById("circle-button").disabled = false;
        document.getElementById("triangle-button").disabled = true;
        document.getElementById("square-button").disabled = false;
    }
    else if(button_shape === "square") {
        document.getElementById("circle-button").disabled = false;
        document.getElementById("triangle-button").disabled = false;
        document.getElementById("square-button").disabled = true;
    }
    else if(button_shape === "finish") {
        document.getElementById("circle-button").disabled = false;
        document.getElementById("triangle-button").disabled = false;
        document.getElementById("square-button").disabled = false;
    }
    else if(button_shape === "start") {
        document.getElementById("circle-button").disabled = true;
        document.getElementById("triangle-button").disabled = false;
        document.getElementById("square-button").disabled = false;
    }
    else if(button_shape === "disable_all") {
        document.getElementById("circle-button").disabled = true;
        document.getElementById("triangle-button").disabled = true;
        document.getElementById("square-button").disabled = true;
    }
}


function red() {
    color = "red";
    set_button_color("red");
}

function green() {
    color = "green";
    set_button_color("green");
}
function blue() {
    color = "blue";
    set_button_color("blue");
}
function magenta() {
    color = "magenta";
    set_button_color("magenta");
}
function circle() {
    shapeType = "circle";
    set_button_shape("circle");
}

function triangle() {
    shapeType = "triangle";
    set_button_shape("triangle");
}

function square() {
    shapeType = "square";
    set_button_shape("square");
}

function clear_canvas() {
    console.log("clear");
    active_canvas_context = active_canvas.getContext('2d');
    active_canvas_context.clearRect(0, 0, active_canvas_context.canvas.width, active_canvas_context.canvas.height);
    active_canvas_context.beginPath();
    make_axis();
    // add clear operation to list
    current_positions.push([-1,-1]);
    current_colors.push("CLEAR");
    current_shape.push("CLEAR");
}

function finish() { 
    set_button_shape("finish");
    set_button_color("finish");
    clear_canvas();
    socket.emit('finish',{"username":username, "colors":current_colors, "shapes":current_shape, "positions":current_positions});
}


function getMousePosition(drawing_canvas, event) {
    let rect = drawing_canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    x = (x / rect.width)* drawing_canvas.width;
    y = (y / rect.height)* drawing_canvas.height;
    return [x,y]
}

function pointer_down(evt) {
    mouse_clicked = true;
    var mousePos = getMousePosition(active_canvas, evt);
    a = [mousePos[0] / ratio, mousePos[1] / ratio]
    console.log(a)
    active_canvas_context = active_canvas.getContext('2d')
    active_canvas_context.strokeStyle = color;
    active_canvas_context.fillStyle = color;
    if(shapeType === "triangle") {
        active_canvas_context.beginPath();
        active_canvas_context.moveTo(a[0], a[1]);
        active_canvas_context.lineTo(a[0]-15, a[1]+20);
        active_canvas_context.lineTo(a[0]+15, a[1]+20);
        active_canvas_context.fill();
    }
    else if (shapeType === "square") {
        active_canvas_context.fillRect(a[0], a[1], 15, 15);
    }
    else {
        active_canvas_context.beginPath();
        active_canvas_context.arc(a[0], a[1], 8, 0, 2 * Math.PI);
        active_canvas_context.fill();
    }
    current_positions.push(a);
    current_colors.push(color);
    current_shape.push(shapeType);
}

function pointer_up(evt) {
    mouse_clicked = false;
}

function startExperiment() {
    console.log("start");
    set_button_shape("start");
    set_button_color("start");
    make_axis();
    socket.emit('start',{"username":username});
}

socket.on('endExperiment', function(data) {
    set_button_shape("disable_all");
    set_button_color("disable_all");
    document.getElementById("finish-button").disabled = true;
    document.getElementById("clear-button").disabled = true;
    alert("Thank you! You are done :) Please fill out the survey at https://forms.gle/YNUEbS38NTkJNNqE8 using code MOON-WILLOW-6.");
});

socket.on('startNextImage', function(data) {
    current_colors = [];
    current_shape = [];
    current_positions = [];
    if(data["instruction_num"] === 0) {
        alert("Welcome!\n\nYour goal is to follow the instruction on the top right to create an image using the buttons on the right. Each instruction belongs to either Type A or Type B - you should follow all instructions the same way, but we will ask you after the study to choose whether you found Type A or Type B instructions easier to follow. \n\nWhen you are done with one image, click ``Finish'' to proceed to the next one. You will create 10 images in total. At the end, you will receive a link to a post-study survey to fill out.\n\nPlease do the task in one sitting (no switching tabs).");
    }
    document.getElementById("description-counter").innerHTML = (data["instruction_num"]+1)+"/10";
    document.getElementById("description-number").innerHTML = "Instruction #"+(data["instruction_num"]+1);
    document.getElementById("description-text").innerHTML = data["instruction_text"];
});