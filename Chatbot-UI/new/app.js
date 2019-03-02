//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
 
var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext; //new audio context to help us record
 
var recordButton = document.getElementById("recordButton");
console.log(recordButton)
var stopButton = document.getElementById("stopButton");
 
//add events to those 3 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
    //console.log("recordButton clicked");
    var constraints = { audio: true, video:false }
    recordButton.disabled = true;
    stopButton.disabled = false;
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        //console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input,{numChannels:1})
        rec.record()
        //console.log("Recording started");
    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
    });
}

function stopRecording() {
    //console.log("stopButton clicked");
    stopButton.disabled = true;
    recordButton.disabled = false;
    rec.stop();
    gumStream.getAudioTracks()[0].stop();
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
    //console.log(blob)   
    var fd = new FormData();
    fd.append('fname', 'test.wav');
    //console.log(fd)
    var reader = new FileReader();
 reader.readAsDataURL(blob); 
 reader.onloadend = function() {
     base64data = reader.result;                
     //console.log(base64data);
    fd.append('data', base64data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5001/voice',
        data: fd,
        processData: false,
        contentType: false,
    }).done(function(data) {
           console.log(data);
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5001/speech',
        data: fd,
        processData: false,
        contentType: false,
    }).done(function(data) {
           //console.log(data);
           clickHandler2(toTitleCase(data));

    var fd2 = new FormData();
    fd2.append('data', data);
$.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5001/say',
        data: fd2,
        processData: false,
        contentType: false,
    }).done(function(data) {
           //console.log(data);
       });
    });
    });
 }
}
function toTitleCase(toTransform) {
  return toTransform.replace(/\b([a-z])/g, function (_, initial) {
      return initial.toUpperCase();
  });
}
function clickHandler2(str) {
        console.log(str)
      $(".card-body")[1].innerHTML+=`<div class="row justify-content-end marign_add3">
             <span class="badge badge-pill badge-info text_receive" id="result">`+str+`</span>
           </div>`;  

            var count = 0;
for(var i = 0; i < emot.length; ++i){
    if(emot[i] == 'sad')
        count++;
}
console.log("COUNT"+count)
if(count>=7)
    str+=" sad"
console.log(str)
      var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://localhost:5005/conversations/default/respond",
        "method": "POST",
        "headers": {
          "content-type": "application/json",
          "cache-control": "no-cache",
          "postman-token": "93e80c0a-3625-8ef5-ac82-07e718b5c7b7"
        },
        "processData": false,
        "data": "{\"query\":\""+str+"\"}"
      }

      $.ajax(settings).done(function (response) {
        //console.log("HERE")
        var result=[];
        var a = response[0]["text"].split("\n")
        //console.log(a)
        var cumm=0;
        for (var i = 0; i <=a.length - 1; i++) {
        texttime(a[i],cumm);
        speechtime(a[i],cumm);
        cumm+=a[i].split(" ").length
      }
      });
      $(".text-input-chat")[0].value="";
    };

function texttime(el,i) { setTimeout(function() { 
$(".card-body")[1].innerHTML+=`<div class="row marign_add3">
             <span class="badge-success text_send" id="result">`+el+`</span>
           </div>`; 
                var elem = document.getElementsByClassName('card-body')[1];
                elem.scrollTop = elem.scrollHeight;
}, i*350); }
function speechtime(el,i) { setTimeout(function() {
var res = el.replace(/<[^>]*>/gi, "");
          responsiveVoice.speak(res);
}, i*350); }