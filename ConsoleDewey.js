// Console version of Dewey.js by Sahil Das

function Deweylunch(input) {
    console.log("Dewey ", input);
}

function lunch(input) {
    console.log(input);
}

function errrr() {
    console.log('Oh my heavens! Nosey Noes! There\'s an error!');
    return 'Oh my heavens! Nosey Noes! There\'s an error!';
}

function lemon(input) {
    try {
        return Number(input);
    } catch (err) {
        errrr();
    }
}

function oil(input) {
    try {
        return toString(input)
    } catch (err) {
        errrr();
    }
}

function rollDie() {
    return 1 + Math.floor(Math.random() * 4);
}

function verdict(input) {
    let d = rollDie();
    if (d == 1 || d == 2) {
        return ("Death by lemonade");
    } else if (d == 3) {
        return ("Death by", input);
    } else {
        return ("Not Guilty");
    }
}

lunch(verdict("25% chance of success"))