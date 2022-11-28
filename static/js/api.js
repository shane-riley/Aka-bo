// All API methods

const API_ROOT = '/api/v1';

const DO_AUTHORIZATION = false;

async function akaAPIRequest(method, absLink, headers, body) {
    // GENERAL API Request method
    if (!absLink || !headers || !body) {
        throw new Error(`Missing a parameter for ${method}.`)
    }
    try {
        const rawResponse = await fetch(absLink, {
            method: method,
            headers: headers,
            body: JSON.stringify(body)
        });
        const content = await rawResponse.json();
        return content;
    }
    catch(err) {
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
    composite = composite.slice(0,-1);
    return composite;
}

// Get token
async function getToken() {


    if (DO_AUTHORIZATION) {
        // TODO: Implement me

        return null;
    }
    else {
        // No auth
        return null;
    }
}

// Make headers
function buildHeaders(auth = null) {
    return {
        "Authorization": (auth) ? auth : "Bearer TOKEN_MISSING"
    };
}

// Firebase ops *********************************************************************
async function fbLogin(username, password) {
    
    if (DO_AUTHORIZATION) {
        // TODO: Use firebase wrapper to login
    }
}

async function fbLogout() {
    
    if (DO_AUTHORIZATION) {
        // TODO: Use firebase wrapper to logout
    }
}

async function fbCreateUser(username, password) {
    
    if (DO_AUTHORIZATION) {
        // TODO: Use firebase wrapper to create user
    }
}

// EXPORTED FUNCTIONS ************************************************************
// User ops **********************************************************************

// Login user
export async function akaLogin(username, password) {
    // Actually just uses Firebase
    return await fbLogin(username, password);
}

export async function akaLogout() {
    // Actually just uses Firebase
    return await fbLogout();
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
    await fbCreateUser(username, password);

    const args = {
        username: username,
        email: email
    };

    return await akaAPIRequest("POST",
                               API_ROOT+urlWithArgs("/user", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("GET",
                               API_ROOT+urlWithArgs("/user", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("PUT",
                               API_ROOT+urlWithArgs("/user", args),
                               buildHeaders(await getToken()),
                               null);
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

    const args = {
        uid: uid
    };

    return await akaAPIRequest("DELETE",
                               API_ROOT+urlWithArgs("/user", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("POST",
                               API_ROOT+urlWithArgs("/matchmaking", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("GET",
                               API_ROOT+urlWithArgs("/matchmaking", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("DELETE",
                               API_ROOT+urlWithArgs("/matchmaking", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("GET",
                               API_ROOT+urlWithArgs("/game", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("PUT",
                               API_ROOT+urlWithArgs("/game", args),
                               buildHeaders(await getToken()),
                               null);
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

    return await akaAPIRequest("DELETE",
                               API_ROOT+urlWithArgs("/game", args),
                               buildHeaders(await getToken()),
                               null);
}
