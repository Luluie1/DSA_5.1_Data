import numpy as np
import torch
from IPython.core.display import display, HTML

def make_prediction_canvas(canvas_size, prediction_func_name):
        canvas_html = '''
<div>
<p>Drawing canvas:</p>
<canvas id="canvas" width="''' + str(canvas_size[0]) + '''" height="''' + str(canvas_size[1]) + '''" style="border: 5px solid black"></canvas>
<button onclick="predict()">Predict</button>
<button onclick="clear_canvas()">Clear canvas</button>
<p id="predictionfield">Prediction:</p>
</div>
<script type="text/Javascript">
function prediction_callback(data){
    if (data.msg_type === 'execute_result') {
        document.getElementById("predictionfield").innerHTML = "Prediction: " + data.content.data['text/plain']
        /*$('#predictionfield').html("Prediction: " + data.content.data['text/plain'])*/
    } else {
        console.log(data)
    }
}
function predict(){
    var imgData = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);
    imgData = Array.prototype.slice.call(imgData.data).filter(function (data, idx) { return idx % 4 == 3; })

    var kernelAPI = undefined
    try {
      //check if defined
      if (IPython) {
        kernelAPI = "IPython"
      }
    } catch(err) {
    }

    try {
      //check if defined
      if (google) {
        kernelAPI = "google"
      }
    } catch(err) {
    }

    if (kernelAPI === "IPython") {
        var command = "''' + prediction_func_name + '''(" + JSON.stringify(imgData) + ")"
        document.getElementById("predictionfield").innerHTML = "Prediction: calculating..."
        /*$('#predictionfield').html("Prediction: calculating...")*/

        var kernel = IPython.notebook.kernel;
        kernel.execute(command, {iopub: {output: prediction_callback}}, {silent: false});
    } else if (kernelAPI === "google") {
        google.colab.kernel.invokeFunction("''' + prediction_func_name + '''", [imgData], {})
        .then(function(result) {
            prediction_callback({msg_type: 'execute_result', content: {data: result.data}})
        })
    } else {
        console.error('no kernel api found to invoke predictions!')
    }
}

canvas = document.getElementById('canvas')
ctx = canvas.getContext("2d")

var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

function clear_canvas() {    
    clickX = new Array();
    clickY = new Array();
    clickDrag = new Array();
    
    redraw();
}

function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
}

var canvas = document.getElementById("canvas")
/*$('#canvas').mousedown(*/
canvas.addEventListener('mousedown', function(e){
  var boundingRect = canvas.getBoundingClientRect()
  var mouseX = e.pageX - boundingRect.left;
  var mouseY = e.pageY - boundingRect.top;
  
  paint = true;
  addClick(mouseX, mouseY);
  redraw();
});

/*$('#canvas').mousemove(*/
canvas.addEventListener('mousemove', function(e){
  if(paint){
    var boundingRect = canvas.getBoundingClientRect()
    addClick(e.pageX - boundingRect.left, e.pageY - boundingRect.top, true);
    redraw();
  }
});

/*$('#canvas').mouseup(*/
canvas.addEventListener('mouseup', function(e){
  paint = false;
});

/*$('#canvas').mouseleave(*/
canvas.addEventListener('mouseleave', function(e){
  paint = false;
});

function redraw(){
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Clears the canvas
  
  ctx.strokeStyle = '#000000';//"#df4b26";
  ctx.lineJoin = "round";
  ctx.lineWidth = 20;
  for(var i=0; i < clickX.length; i++) {
    ctx.beginPath();
    if(clickDrag[i] && i){
      ctx.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       ctx.moveTo(clickX[i]-1, clickY[i]);
     }
     ctx.lineTo(clickX[i], clickY[i]);
     ctx.closePath();
     ctx.stroke();
  }
}
</script>
'''
        display(HTML(canvas_html)) 

