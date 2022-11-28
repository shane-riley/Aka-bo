import { MD5 } from "./crypto.js"
import { akaPost, akaGet, akaPut, akaDelete, buildHeaders, buildBody} from "./api.js"



// FORM LISTENERS *******************************************
const userCreationForm = document.querySelector("#userCreationForm");
if (userCreationForm) {
    userCreationForm.addEventListener("submit", async function(e) {

        // Prevent a reload
        e.preventDefault();

        // Build headers and body from form
        const headers = buildHeaders(/* No auth */);
        const body = buildBody(this);

        // Encrypt password
        body.encrypted_password = MD5(body.password);
        delete body.password;

        // Perform the API call
        const response = await akaPost('/user', headers, body);
        console.log(response);
    });
}