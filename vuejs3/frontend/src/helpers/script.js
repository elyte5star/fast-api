
import Swal from 'sweetalert2/dist/sweetalert2';

/* eslint-disable */
export const decodeJwtResponse = (token) => {
    let base64Url = token.split(".")[1];
    let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    let jsonPayload = decodeURIComponent(
        window
            .atob(base64)
            .split("")
            .map(function (c) {
                return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join("")
    );
    console.log(JSON.parse(jsonPayload));
    return JSON.parse(jsonPayload);
}

export const isUserNameValid = (username) => {
    /* 
      Usernames can only have: 
      - Lowercase Letters (a-z) 
      - Numbers (0-9)
      - Dots (.)
      - Underscores (_)
    */
    const res = /^[a-z0-9_\.]+$/.exec(username);
    const valid = !!res;
    return valid;
}


export const postToTokenEndpoint = async (url = "", data = {}) => {
    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data // JSON.stringify(data)
    }
    const response = await fetch(url, options);
    return response.json();
}

export const show_add_entry = (id) => {
    let element = document.getElementById(id);
    element.style.display = "";

}

export const hide_add_entry = (id) => {
    let element = document.getElementById(id);
    element.style.display = "none";
}

function is_valid_Email(email) {
    return email.match(
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}

function isValidTel(tel) {
    // check for allowed characters using a regular expression
    const re = /^[0-9()+\-\s]*$/
    return re.test(tel);
}

export const  is_Input_Error = (name, email, password, password_, tel) =>{
    if (name.length == 0) {
        return Swal.fire("Empty username!");
    }
    else if (email.length == 0) {
        return Swal.fire(" Empty email field!");
    }
    else if (tel.length == 0) {

        return Swal.fire("Empty Telephone field!");
    }
    else if (password.length == 0 || password_.length == 0) {
        return Swal.fire(" Empty Password Field!");
    }
    else if (password !== password_) {
        return Swal.fire(" Invalid Credentials.Password mismatch!");
    }
    // check for valid telephone
    else if (tel.length > 0 && !isValidTel(tel)) {
        return Swal.fire("Invalid letters for telephone!");
    }
    // check for valid email
    else if (email.length > 0 && !is_valid_Email(email)) {
        Swal.fire("Invalid email address!");
    }
    // check for valid letters
    else if (name.length > 0 && !isUserNameValid(name)) {
        return Swal.fire(" Invalid letters for username!");
    }
    // no error
    else {
        return false;
    }
    return true;
}