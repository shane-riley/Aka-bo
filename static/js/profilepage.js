import {akaGetUser, akaAuthStateChanged, fbUser, akaUpdateUser} from "./api.js"

// Redirect on login
akaAuthStateChanged((user) => { 
    if (user) {
        
        // Grab data
        akaGetUser(fbUser().uid).then((u) => draw(u));

    } else {
        // Go to login
        window.location.href = "/login";
    }
});

// Draw user
function draw(user) {
    // Populate data
    document.querySelector("#username").innerHTML = user.username;
    document.querySelector("#wins").innerHTML = user.wins;
    document.querySelector("#losses").innerHTML = user.losses;
    document.querySelector("#bio").value = user.bio;
}

// Logout
function updateBio() {
    
    const newBio = document.querySelector("#bio").value;

    // Update bio
    akaUpdateUser(fbUser().uid, newBio).then((u) => draw(u));
}

document.querySelector("#updatebiobutton").addEventListener('click', updateBio, false);