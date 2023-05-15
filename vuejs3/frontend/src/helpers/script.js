
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