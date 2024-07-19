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

function DeweyGenerateName() {
        const date = new Date();
        const vowels = ['a', 'e', 'i', 'o', 'u', 'y'];
        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const currentDayOfWeek = daysOfWeek[date.getDay()];
        if (currentDayOfWeek === 'Friday' || currentDayOfWeek === 'Saturday') {
                
const consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'];
                let single = consonants[Math.floor(Math.random()*vowels.length)] + vowels[Math.floor(Math.random()*vowels.length)]
                return `${single} ${single}`
        }
        else {if (currentDayOfWeek == 'Monday') {
                var names = [
                        "No No",
                        "AA OO",
                        "Plums",
                        "Seriously",
                        "Hater Of Monday"
                ];

                return names[Math.floor(Math.random()*names.length)];
        } else {
                var names = [
                        "Joe",
                        "Ben",
                        "Mary",
                        "Gary",
                        "Hazel"
                ]
                var adjectives = [
                        "Fantastic",
                        "Triumphant",
                        "Happy",
                        "Cheesy",
                        "Simply Mad"
                ]
                return `${adjectives[Math.floor(Math.random()*adjectives.length)]} ${names[Math.floor(Math.random()*names.length)]}`
        }}
}
