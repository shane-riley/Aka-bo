// Imports
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.14.0/firebase-app.js"
import { getAuth, setPersistence, onAuthStateChanged, browserSessionPersistence, createUserWithEmailAndPassword, signInWithEmailAndPassword, deleteUser, signOut, getIdToken } from "https://www.gstatic.com/firebasejs/9.14.0/firebase-auth.js"

// Constants
const API_ROOT = '/api/v1';
const DO_AUTHORIZATION = true;

// Init firebase whenever this file is pulled
const firebaseConfig = {
    apiKey: "AIzaSyC9fHWrPTpYImvef53lTOEq6WNgzcxoMhU",
    authDomain: "projectsandbox-365201.firebaseapp.com",
    projectId: "projectsandbox-365201",
    storageBucket: "projectsandbox-365201.appspot.com",
    messagingSenderId: "906527119033",
    appId: "1:906527119033:web:b9fccade68a222b2126d68"
};

// Startup ops

// Initialize app
export const FB_APP = initializeApp(firebaseConfig);
export const FB_AUTH = getAuth(FB_APP);

onAuthStateChanged(getAuth(FB_APP), (user) => {
    if (user) {
        console.log(`Logged in: ${user.uid}`);
    } else {
        console.log("Logged out.");
    }
});


// API ops

export function akaAuthStateChanged(b) { onAuthStateChanged(getAuth(FB_APP), b); }

async function akaAPIRequest(method, absLink, headers) {
    // GENERAL API Request method
    // No JSON bodies supported
    if (!absLink || !headers) {
        throw new Error(`Missing a parameter for ${method}.`)
    }
    try {
        const rawResponse = await fetch(absLink, {
            method: method,
            headers: headers,
        });

        const content = await rawResponse.json();
        return content;
    }
    catch (err) {
        console.error(`Error at fetch ${method}: ${err}`);
        throw err;
    }
}

function urlWithArgs(url, args) {
    // url is address to ping
    // args are key value args

    // Short circuit if no args
    if (args === null || Object.keys(args).length === 0) {
        return url;
    }

    // Start the query
    let composite = url + "?";

    for (const [key, value] of Object.entries(args)) {
        // Add the key value pair
        composite = composite.concat(key + "=" + value);

        // Add an ampersand
        composite = composite + "&";

    }
    // Last char is a hanging ampersand--drop it
    composite = composite.slice(0, -1);
    return composite;
}

// Get token
async function fbGetToken() {

    if (DO_AUTHORIZATION && akaIsLoggedIn()) {
        return await getIdToken(fbUser(), false);
    }
    else {
        // No auth
        return null;
    }
}

export function akaIsLoggedIn() {
    if (!DO_AUTHORIZATION) return true;

    return fbUser() !== null;
}

export function fbUser() {
    if (!DO_AUTHORIZATION) return null;
    return getAuth(FB_APP).currentUser
}

// Make headers
function buildHeaders(auth = null) {
    return {
        "Authorization": (auth) ? auth : "Bearer TOKEN_MISSING"
    };
}

// Firebase ops *********************************************************************
async function fbLogin(email, password) {

    if (DO_AUTHORIZATION) {
        // Use firebase wrapper to login
        return signInWithEmailAndPassword(getAuth(FB_APP), email, password);
    }
}

async function fbLogout() {

    if (DO_AUTHORIZATION) {
        // Use firebase wrapper to logout
        return signOut(getAuth(FB_APP));
    }
}

async function fbCreateUser(email, password) {

    if (DO_AUTHORIZATION) {
        // Use firebase wrapper to create user
        return createUserWithEmailAndPassword(getAuth(FB_APP), email, password);
    }
}

async function fbDeleteUser() {

    if (DO_AUTHORIZATION && akaIsLoggedIn()) {
        // Use firebase wrapper to create user
        return deleteUser(fbUser());
    }
}

// EXPORTED FUNCTIONS ************************************************************
// User ops **********************************************************************

// Login user
export async function akaLogin(username, password) {
    // Actually just uses Firebase
    // Throw if fails
    return fbLogin(username, password);
}

export async function akaLogout() {
    // Actually just uses Firebase
    // Throw if fails
    return fbLogout();
}

// Create user
export async function akaCreateUser(username, email, password) {

    // POST request
    // Args:
    // username: public-facing username
    // email: email address
    // uid: (from token)
    // TOKEN REQUIRED (if auth on)

    // Returns a User object on success (see Python class User)
    // Throws a exception with message on failure

    // Begin with the firebase ops

    // TODO: Create user with username and password (assume token stored at this point)
    // Only if auth on

    // Must wait to get token
    await fbCreateUser(email, password);

    const args = {
        username: username,
        email: email
    };

    return akaAPIRequest("POST",
        API_ROOT + urlWithArgs("/user", args),
        buildHeaders(await fbGetToken()));
}


// Get user
export async function akaGetUser(uid) {

    // If auth is off, uid is same as username

    // GET request
    // Args:
    // uid: uid of user to poll (not necessarily the client uid)
    // TOKEN REQUIRED (if auth on)

    // Returns a User object on success (see Python class User)
    // Throws a exception with message on failure

    const args = {
        uid: uid
    };

    return akaAPIRequest("GET",
        API_ROOT + urlWithArgs("/user", args),
        buildHeaders(await fbGetToken()));
}


// Update user
export async function akaUpdateUser(uid, bio) {

    // If auth is off, uid is same as username

    // PUT request
    // Args:
    // uid: (ONLY required if auth is off) user to update
    // bio: new user bio

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, use token uid taken over function arg

    // Returns a User object on success (see Python class User)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        bio: bio
    };

    return akaAPIRequest("PUT",
        API_ROOT + urlWithArgs("/user", args),
        buildHeaders(await fbGetToken()));
}


// Delete user
export async function akaDeleteUser(uid) {

    // If auth is off, uid is same as username

    // DELETE request
    // Args:
    // uid: (ONLY required if auth is off) user to remove

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a User object on success (see Python class User)
    // Throws a exception with message on failure

    // Drop user
    fbDeleteUser();

    const args = {
        uid: uid
    };

    return akaAPIRequest("DELETE",
        API_ROOT + urlWithArgs("/user", args),
        buildHeaders(await fbGetToken()));
}


// Match ops **********************************************************************

// Create Ticket
export async function akaCreateTicket(uid) {

    // If auth is off, uid is same as username

    // POST request
    // Args:
    // uid: (ONLY required if auth is off) user to own ticket

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a MatchTicket object on success (see Python class MatchTicket)
    // Throws a exception with message on failure

    const args = {
        uid: uid
    };

    return akaAPIRequest("POST",
        API_ROOT + urlWithArgs("/matchmaking", args),
        buildHeaders(await fbGetToken()));
}


// Poll Ticket
export async function akaPollTicket(ticket_uuid, uid) {

    // If auth is off, uid is same as username

    // GET request
    // Args:
    // ticket_uuid: ticket identifier
    // uid: (ONLY required if auth is off) user that owns ticket

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a MatchTicket object on success (see Python class MatchTicket)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        uuid: ticket_uuid
    };

    return akaAPIRequest("GET",
        API_ROOT + urlWithArgs("/matchmaking", args),
        buildHeaders(await fbGetToken()));
}


// Delete Ticket
export async function akaDeleteTicket(ticket_uuid, uid) {

    // If auth is off, uid is same as username

    // DELETE request
    // Args:
    // ticket_uuid: ticket identifier
    // uid: (ONLY required if auth is off) user that owns ticket

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a MatchTicket object on success (see Python class MatchTicket)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        uuid: ticket_uuid
    };

    return akaAPIRequest("DELETE",
        API_ROOT + urlWithArgs("/matchmaking", args),
        buildHeaders(await fbGetToken()));
}


// Game ops **********************************************************************

// Poll game
export async function akaPollGame(game_uuid, uid) {

    // If auth is off, uid is same as username

    // GET request
    // Args:
    // game_uuid: game identifier
    // uid: (ONLY required if auth is off) user playing game

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a Game object on success (see Python class Game)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        uuid: game_uuid
    };

    return akaAPIRequest("GET",
        API_ROOT + urlWithArgs("/game", args),
        buildHeaders(await fbGetToken()));
}


// Make Move
export async function akaMakeMove(game_uuid, uid, move) {

    // If auth is off, uid is same as username

    // PUT request
    // Args:
    // game_uuid: game identifier
    // uid: (ONLY required if auth is off) user playing game
    // move: column to drop

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a Game object on success (see Python class Game)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        uuid: game_uuid,
        move: move
    };

    return akaAPIRequest("PUT",
        API_ROOT + urlWithArgs("/game", args),
        buildHeaders(await fbGetToken()));
}


// Forfeit Game
export async function akaForfeitGame(game_uuid, uid) {

    // If auth is off, uid is same as username

    // DELETE request
    // Args:
    // game_uuid: game identifier
    // uid: (ONLY required if auth is off) user playing game

    // TOKEN REQUIRED (if auth on)
    // IF AUTH ON, user token uid taken over function arg

    // Returns a Game object on success (see Python class Game)
    // Throws a exception with message on failure

    const args = {
        uid: uid,
        uuid: game_uuid
    };

    return akaAPIRequest("DELETE",
        API_ROOT + urlWithArgs("/game", args),
        buildHeaders(await fbGetToken()));
}
