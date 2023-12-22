const socket = new WebSocket("ws://localhost:5003");

let Name = document.getElementById("Name");
function SendConsoleMessage(){
    socket.send(Name.value);
}

socket.onopen = function(e){
    console.log("[open] Connection established");
    socket.send("My name is John");
};

socket.onclose = function(event){
    console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
};

socket.onmessage = function(event){
    console.log(`[message] Data received from server: ${event.data}`);
};