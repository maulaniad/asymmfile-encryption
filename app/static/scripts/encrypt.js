const pValue = document.getElementById('p');
const qValue = document.getElementById('q');
const nValue = document.getElementById('n');
const mValue = document.getElementById('m');
const eValue = document.getElementById('e');
const dValue = document.getElementById('d');
const keyRSA = document.getElementById('keyRSA');

function isPrime(num) {
    if (num < 2) return false;
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false;
    }
    return true;
}

function getRandomPrime() {
    let randomNum = Math.floor(Math.random() * 100) + 1;
    while (!isPrime(randomNum)) {
        randomNum = Math.floor(Math.random() * 100) + 1;
    }
    return randomNum;
}

pValue.value = getRandomPrime();
qValue.value = getRandomPrime();
nValue.value = pValue.value * qValue.value;
mValue.value = (pValue.value - 1) * (qValue.value - 1);
eValue.value = 0;
dValue.value = 0;
keyRSA.value = 0;

