'use strict';

// TODO: LOAD UPLOADED PIC ON PROFILE PAGE

// alert("create-event.js is connected!");

//when you click "Upload Image"
var loadFile = function(event) {
    //grab 
    var image = document.getElementById('output');
    //create a URL out of the uploaded image file
    console.log(image);
    
    image.src = URL.createObjectURL(event.target.files[0]);
    
};
 