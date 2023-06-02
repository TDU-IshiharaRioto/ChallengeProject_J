window.onload = function() {
    function updateTime() {
        const now = new Date();
        const seconds = now.getSeconds();
        const minutes = now.getMinutes();
        const hours = (now.getHours() % 12) + minutes / 60;

        document.querySelector('.second-hand').style.transform = `rotate(${seconds * 6}deg)`;
        document.querySelector('.minute-hand').style.transform = `rotate(${minutes * 6}deg)`;
        document.querySelector('.hour-hand').style.transform = `rotate(${hours * 30}deg)`;
    }

    setInterval(updateTime, 1000);
    updateTime();
}
