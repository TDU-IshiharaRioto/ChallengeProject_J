window.onload = function() {
    const svg = document.getElementById('clock');

    function updateTime() {
        const now = new Date();
        const seconds = now.getSeconds();
        const minutes = now.getMinutes();
        const hours = (now.getHours() % 12) + minutes / 60;

        const secondHand = svg.querySelector('.second-hand');
        secondHand.setAttribute('transform', `rotate(${seconds * 6}, 50, 50)`);

        const minuteHand = svg.querySelector('.minute-hand');
        minuteHand.setAttribute('transform', `rotate(${minutes * 6}, 50, 50)`);

        const hourHand = svg.querySelector('.hour-hand');
        hourHand.setAttribute('transform', `rotate(${hours * 30}, 50, 50)`);
    }

    setInterval(updateTime, 1000);
}

