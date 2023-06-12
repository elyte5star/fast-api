import { userAuthStore } from "@/stores/auth_store";
import Swal from 'sweetalert2/dist/sweetalert2';
export const fetchMethodWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE')
};



function request(method) {
    return (url, body) => {
        const requestOptions = {
            method,
            headers: authHeader(url)
        };
        if (body) {
            requestOptions.headers['Content-Type'] = 'application/json';
            requestOptions.body = JSON.stringify(body);
        }
        return fetch(url, requestOptions).then(handleResponse);
    }
}




function authHeader(url) {
    // return auth header with jwt if user is logged in and request is to the api url
    const { user } = userAuthStore();
    const isLoggedIn = !!user?.access_token;
    const isApiUrl = url.startsWith(process.env.VUE_APP_API_URL);
    if (isLoggedIn && isApiUrl) {
        return { Authorization: 'Bearer ' + user.access_token };
    } else {
        return {};
    }
}


async function handleResponse(response) {
    const isJson = response.headers?.get('content-type')?.includes('application/json');
    const data = isJson ? await response.json() : null;
    // check for error response
    if (!response.ok) {
        const { user, logout } = userAuthStore();
        if ([401, 403].includes(response.status) && user) {
            // auto logout if 401 Unauthorized or 403 Forbidden response returned from api
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "Session Expired",
                confirmButtonText: 'Home',
                footer: '<a href="/login">Please, log in again!.</a>'
            })
            logout();
        }
        // get error message from body or default to response status
        const error = (data && data.message) || response.status;
        return Promise.reject(error);
    }

    return data;
}


