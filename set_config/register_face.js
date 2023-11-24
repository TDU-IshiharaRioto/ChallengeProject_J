const video = document.getElementById('video');

// getUserMedia()を使用してWebカメラを起動
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        // ビデオ要素にストリームを設定
        video.srcObject = stream;
        // ビデオを再生
        video.play();
    })
    .catch(error => {
        console.error('Webカメラの起動に失敗しました。', error);
        if(error == 'NotAllowedError: Permission denied'){
            alert('カメラの使用を許可してください。');
        }
    });

// ビデオ要素をDOMに追加
document.body.appendChild(video);

// キャプチャしたフレームを保存するためのキャンバス要素を作成
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

// http通信関連
const xhr = new XMLHttpRequest();

// ビデオからフレームをキャプチャ
async function captureFrame() {
    // キャンバスのサイズをビデオのサイズに合わせる
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // ビデオからフレームをキャプチャしてキャンバスに描画
    data = [];
    for(let i = 0; i < 10; i++){
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        dataURL = canvas.toDataURL();
        data.push(dataURL);
        // console.log(dataURL);
    
        await new Promise(resolve => setTimeout(resolve, 250));
    }

    xhr.open('POST', 'http://localhost:8080', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    xhr.onload = function() {
        console.log('onload');
        if (xhr.status >= 200 && xhr.status < 400) {
            var response = xhr.responseText;
            console.log(response);
        } else {
            console.error('リクエストに失敗しました。', xhr.status, xhr.statusText);
        }
    };

    xhr.onerror = function() {
        console.error('エラーが発生しました。');
    };

    xhr.ontimeout = function() {
        console.error('timeout');
    };

    xhr.onabort = function() {
        console.error('abort');
    };

    xhr.send(data);
}