var webSocket = new WebSocket("ws://localhost:9998");

Reference: https://www.nowonbun.com/247.html [明月の開発ストーリ]
window.onload = function() {
    const timeElement = document.getElementById('time');
    
    const yobi= new Array("日","月","火","水","木","金","土");


    
    function updateTime() {
        const now = new Date();
        const year = now.getFullYear().toString().padStart(4, '0');
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const day = now.getDate().toString().padStart(2, '0');
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');

        const week = now.getDay();
        timeElement.textContent = `  ${month}/${day} (${yobi[week]})  ${hours}:${minutes}:${seconds}`;
    }

    setInterval(updateTime, 1000);
}

webSocket.onopen = function(message){
    console.log("connect");
    webSocket.send('東京都');
    
};

webSocket.onmessage = function(message){
    var msg = message.data;
    msg = msg.replace(/'/g,"\"");
    obj = JSON.parse(msg);

    const weatherElement = document.getElementById('weather');
    weatherElement.textContent = obj["0"]["weather"] + " " + obj["0"]["maxtemp"] + "℃ / " + obj["0"]["mintemp"] + "℃";


};
