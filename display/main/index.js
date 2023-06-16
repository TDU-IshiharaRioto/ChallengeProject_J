window.onload = function() {
    const timeElement = document.getElementById('time');
    const weatherElement = document.getElementById('weather');
    const yobi= new Array("日","月","火","水","木","金","土");
    
    var req = new XMLHttpRequest();		  // XMLHttpRequest オブジェクトを生成する
    req.onreadystatechange = function() {		  // XMLHttpRequest オブジェクトの状態が変化した際に呼び出されるイベントハンドラ
        if(req.readyState == 4 && req.status == 200){ // サーバーからのレスポンスが完了し、かつ、通信が正常に終了した場合
        //alert(req.responseText);		          // 取得した JSON ファイルの中身を表示
        const jsonObj = JSON.parse(req.responseText);

        for (let item of jsonObj) {
            console.log("date: " + item.date + " weather: " + item.weather + " max-temp: " + item.max-temp + " min-temp: " + item.min-temp);
        }
        }
    };
    req.open("GET", "http://127.0.0.1/ChallengeProject_J/weather.json", false); // HTTPメソッドとアクセスするサーバーのURLを指定
    req.send(null);					    // 実際にサーバーへリクエストを送信


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
