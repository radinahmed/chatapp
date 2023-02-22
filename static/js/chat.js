const socket = new WebSocket('ws://' + window.location.host + '/websocket');
let webRTCConnection;
const sendelement = document.getElementsByClassName("btn");
sendelement[0].addEventListener("click", sendMessage);

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;
    chatBox.value = "";
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({'messageType': 'chatMessage', 'comment': comment}));
    }
}



// called when the page loads to get the chat_history
//function get_chat_history() {
//    const request = new XMLHttpRequest();
 //   request.onreadystatechange = function () {
 //       if (this.readyState === 4 && this.status === 200) {
 //          const messages = JSON.parse(this.response);
  //          for (const message of messages) {
 //               addMessage(message);
  //          }
 //       }
 //   };
  //  request.open("GET", "/chat-history");
  //  request.send();
//}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    console.log(ws_message);
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType

    switch (messageType) {
        case 'chatMessage':
            addMessage(message);
            break;
        case 'webRTC-offer':
            webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
            webRTCConnection.createAnswer().then(answer => {
                webRTCConnection.setLocalDescription(answer);
                socket.send(JSON.stringify({'messageType': 'webRTC-answer', 'answer': answer}));
            });
            break;
        case 'webRTC-answer':
            webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
            break;
        case 'webRTC-candidate':
            webRTCConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            break;
        default:
            console.log("received an invalid WS messageType");
    }
}



function welcome() {
    document.getElementById("paragraph").innerHTML += "<br/>This text was added by JavaScript 😀"

  //  get_chat_history()

    // use this line to start your video without having to click a button. Helpful for debugging
    // startVideo();
}
//after websockets code
var cookieList = (document.cookie) ? document.cookie.split('; ') : [];
console.log(cookieList)
function myFunction() {
    alert("User already exists, try a new username");
}
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

const userexists= getCookie('userexists')
const currentuser= getCookie('name')
console.log(currentuser)
console.log(userexists)
console.log(currentuser)
if(userexists=="True"){
    myFunction();
}

var closebtns = document.getElementsByClassName("close");
var i;

// Loop through the elements, and hide the parent, when clicked on
for (i = 0; i < closebtns.length; i++) {
  closebtns[i].addEventListener("click", function() {
    this.parentElement.style.display = 'none';
  });
}


function splitbyleng(ster) {
  ster1= ster
  maxlen=16
  ster2=""
  strleng= ster.length;
  if(strleng<16){
    for (let i=0 ; i<strleng; i++){
      ster2+=ster1[i]
  
    }

  }
  else{
    for (let i=0 ; i<16; i++){
      ster2+=ster1[i]
  
    }

  }
 
  return ster2
}


function skipbyleng(ster) {
  ster1= ster
  maxlen=16
  ster2=""
  strlen= ster.length
  if(strlen<16){
    return ster1
  }
  else{
    return ster1.slice(16)
  }
}

var h=6
// Renders a new chat message to the page
function addMessage(chatMessage) {
 
  var div = document.getElementsByClassName('p7');
  div=div[0]
//if len of string is greater than 16, divide sring by 16 and break into new lines
  let string1 =chatMessage['username'] + ": " + chatMessage["comment"];
  let length1 = string1.length;

  i=0
  text=""
  while(i < length1){
    if(string1!=""){
      spaces= " &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;"
      text += splitbyleng(string1) + "<br>";
      string1= skipbyleng(string1)
      console.log(string1);
      i+=16;
    }
 
  }
  console.log(currentuser)
  console.log(chatMessage['username'])
  if(chatMessage['username']==currentuser){
    console.log("same")
    console.log(text)
    var text = text.replace('undefined','');
    console.log(text)
    let demo=document.createElement('p')
    demo.id='demo'+h.toString();
    demo.style.position= "absolute"
    demo.style.right= "10%"
    demo.innerHTML= "<span style=\"position: relative;left:48%;font-size:10px; \">"+text+"</span>"
    div.innerHTML+=demo.innerHTML
    h++
  }
  else{
    console.log(text)
    var text = text.replace('undefined','');
    console.log(text)
    let demo=document.createElement('p')
    demo.id='demo'+h.toString();
    demo.style.position= "absolute"
    demo.style.right= "10%"
    demo.innerHTML= text
    div.innerHTML+=demo.innerHTML
    h++
  }
  
}
//"<span style=\"position: absolute;right: 10%;margin: 0;\"</span>"
//to render messages on columns, set a sender and receiver via cookie. 
//All sender messages appear right, anything else on left. 
// Establish a WebSocket connection with the server
