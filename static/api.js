const API_ROOT = '/api/v1';

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

// EXPORTED FUNCTIONS

// POST wrapper
export async function akaPost(relLink, headers, body)
{
    return await akaAPIRequest("POST", API_ROOT+relLink, headers, body);
}

// PUT wrapper
export async function akaGet(relLink, headers, body)
{
    return await akaAPIRequest("GET", API_ROOT+relLink, headers, body);
}


// PUT wrapper
export async function akaPut(relLink, headers, body)
{
    return await akaAPIRequest("PUT", API_ROOT+relLink, headers, body);
}

// DELETE wrapper
export async function akaDelete(relLink, headers, body)
{
    return await akaAPIRequest("DELETE", API_ROOT+relLink, headers, body);
}

// Make headers
export function buildHeaders(auth = null) {
    return {
        "Content-Type": "application/json",
        "Authorization": (auth) ? auth : "Bearer TOKEN_MISSING"
    };
}

// Make body
export function buildBody(form = null) {
    const data = {};
    for (const pair of new FormData(form)) {
        data[pair[0]] = pair[1];
    }
    return data;
}