const pValue = document.getElementById('p');
const qValue = document.getElementById('q');
const nValue = document.getElementById('n');
const mValue = document.getElementById('m');
const eValue = document.getElementById('e');
const dValue = document.getElementById('d');
const keyRSA = document.getElementById('keyRSA');
const keyTable = document.getElementById('key_table');
const regButton = document.getElementById('regenerate');

function isPrime(num) {
    console.log("EUY");
    if (num < 2) return false;
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false;
    }
    return true;
}

function getRandomPrime() {
    let primeNum = Math.floor(Math.random() * 100) + 1;
    while (!isPrime(primeNum)) {
        primeNum = Math.floor(Math.random() * 100) + 1;
    }
    return primeNum;
}

function setNum() {
    qValue.value = getRandomPrime();
    pValue.value = getRandomPrime();
    nValue.value = pValue.value * qValue.value;
    mValue.value = (pValue.value - 1) * (qValue.value - 1);
    eValue.value = 0;
    dValue.value = 0;
    keyRSA.value = 123;
}

function getCode() {
    fetch('')
        .then(res => res.text()
            .then(res => console.log(res)))
        .catch(err => console.log(err));
}

document.addEventListener("DOMContentLoaded", setNum);
regButton.addEventListener('click', setNum);
