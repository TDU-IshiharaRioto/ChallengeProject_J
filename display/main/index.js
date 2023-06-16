window.onload = function() {
    const data = require('./data.json');
    const timeElement = document.getElementById('time');
    const weatherElement = document.getElementById('weather');
    const yobi= new Array("日","月","火","水","木","金","土");
    const json = `{ "date": "2023-6-13","hour":"14", "weather": "晴れ", "maxtemp": "25","mintemp": "18" }`;
    const parsed = JSON.parse(json);

    weatherElement.textContent = `[${parsed.weather}]  ${parsed.maxtemp}/${parsed.mintemp}℃`;
    var url = '127.0.0.1/ChallengeProject_J/weather.json';
    $.getJSON(url, function(data){
    console.log('data : ', data);
    });
    
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
