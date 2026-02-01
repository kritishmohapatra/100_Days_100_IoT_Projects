function ledOn() {
    fetch('/led/on');
}

function ledOff() {
    fetch('/led/off');
}

function updateStatus() {
    fetch('/led/state')
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText =
                data.value ? "ON" : "OFF";
        });
}

setInterval(updateStatus, 1000);
updateStatus();
