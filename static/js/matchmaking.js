import { fbUser, akaCreateTicket, akaPollTicket, akaDeleteTicket, akaAuthStateChanged } from "./api.js"

let ticket = null;

// Redirect on login
akaAuthStateChanged((user) => { 
    if (user) {

        // Draw the page
        draw(ticket);

    } else {
        window.location.href = "/login";
    }
});


// Draw
function draw(t) {
    ticket = t;
    if (t) {
        console.log(`Ticket: ${t.uuid}`);
        if (t.gameuuid) {
            console.log(`Game found: ${t.gameuuid}`);

            //Store game uuid
            sessionStorage.setItem("gameuuid", t.gameuuid);

            // Hide both buttons
            document.querySelector("#joinButton").style.display = "none";
            document.querySelector("#leaveButton").style.display = "none";
            document.querySelector("#gameFound").style.display = "";

            setTimeout(window.location.href="/game", 1000);

            // Move to game in a sec
        } else {
            // Ticket
            // Hide take button
            document.querySelector("#joinButton").style.display = "none";
            document.querySelector("#leaveButton").style.display = "";

            // Call again in two seconds
            setTimeout(updateTicket, 4000);
        }
    } else {
        console.log("No ticket.");
        // No ticket
        // Hide leave button
        document.querySelector("#joinButton").style.display = "";
        document.querySelector("#leaveButton").style.display = "none";
    }
}

// Update ticket
function updateTicket() {
    if (ticket && ticket.uuid) {
        akaPollTicket(ticket.uuid, fbUser().uid).then((t) => draw(t));
    }
}

// Grab ticket
function takeTicket() {
    akaCreateTicket(fbUser().uid).then((t) => draw(t));
}

// Drop ticket
function dropTicket() {
    if (ticket && ticket.uuid) {
        akaDeleteTicket(ticket.uuid, fbUser().uid).then(() => draw(null));
    }
}

document.querySelector("#joinButton").addEventListener('click', takeTicket, false);
document.querySelector("#leaveButton").addEventListener('click', dropTicket, false);