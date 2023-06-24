var webSocket = new WebSocket("ws://localhost:9998");

Reference: https://www.nowonbun.com/247.html [明月の開発ストーリ]
window.onload = function() {
    const timeElement = document.getElementById('time');
    const weatherElement = document.getElementById('weather');
    const yobi= new Array("日","月","火","水","木","金","土");

    let new_element1 = document.createElement('li');
    new_element1.classList.add("list-group-item");
    new_element1.textContent = ' 遅延';

    let new_element2 = document.createElement('li');
    new_element2.classList.add("list-group-item");
    new_element2.textContent = ' 遅延2';

    document.getElementById("traffic").appendChild(new_element1);
    document.getElementById("traffic").appendChild(new_element2);

    
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
    webSocket.send('weather');
    
};

webSocket.onmessage = function(message){
    console.log(JSON.stringify(message.data));
};
