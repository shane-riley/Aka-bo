import {akaLogout, fbIsLoggedIn} from "./api.js"

var logout = document.getElementById("Logout").addEventListener("click", LogOut, false);

function LogOut(){
    akaLogout();
    console.log(fbIsLoggedIn); 
}