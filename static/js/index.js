import {akaLogout, akaAuthStateChanged} from "./api.js"

// Redirect on login
akaAuthStateChanged((user) => { 
    if (user) {
        // Hide login
        document.querySelector("#loginbutton").style.display = "none";
        document.querySelector("#logoutbutton").style.display = "";
        document.querySelector("#profilebutton").style.display = "";

        // Wire logout
        document.querySelector("#logoutbutton").addEventListener("click", handleLogOut, false);
    } else {
        // Hide profile, mm, logout
        document.querySelector("#loginbutton").style.display = "";
        document.querySelector("#logoutbutton").style.display = "none";
        document.querySelector("#profilebutton").style.display = "none";
    }
});

// Logout
function handleLogOut() {
    akaLogout();
}