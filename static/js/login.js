import {fbIsLoggedIn, akaLogin, akaCreateUser, akaLogout} from "./api.js"

/**
* initApp handles setting up UI event listeners and registering Firebase auth listeners:
*  - firebase.auth().onAuthStateChanged: This listener is called when the user is signed in or
*    out, and that is where we update the UI.
*/
function initApp() {
// Listening for auth state changes.
if(fbIsLoggedIn == true)
{
   window.location.replace("index.html");
}
document.getElementById('quickstart-sign-in').addEventListener('click', toggleSignIn, false);
document.getElementById('quickstart-sign-up').addEventListener('click', handleSignUp, false);
}

window.onload = function() {
initApp();
};

/**
* Handles the sign in button press.
*/
function toggleSignIn() {
var email = document.getElementById('email').value;
var password = document.getElementById('password').value;

akaLogin(email, password); 
}

/**
 * Handles the sign up button press.
 */
function handleSignUp() {
var email = document.getElementById('newEmail').value;
var password = document.getElementById('newPassword').value;
var userName = document.getElementById('newUsername').value;
akaCreateUser(userName, email, password);
}

console.log(fbIsLoggedIn);