const video = document.getElementById('video');
const socket = new WebSocket("ws://localhost:5003");

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

// ビデオからフレームをキャプチャ
async function captureFrame() {
    // キャンバスのサイズをビデオのサイズに合わせる
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // ビデオからフレームをキャプチャしてキャンバスに描画
    data = [];
    for(let i = 0; i < 10; i++){
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL();

        const encoded = btoa(dataURL);
        console.log(encoded);
        data.push(encoded);
    
        await new Promise(resolve => setTimeout(resolve, 250));
    }
    
    data.forEach(elem => {
    // 文字数が原因っぽい
    // 分割して送ってみる？
        socket.send("test");
        console.log(typeof(elem));
    });
}
