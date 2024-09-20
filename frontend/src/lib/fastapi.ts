type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

interface Params {
    [key: string]: any;
}

type Callback = (response: any) => void;

const fastapi = (
    method: HTTPMethod,
    url: string,
    params: Params,
    successCallback?: Callback,
    failureCallback?: Callback,
    token?: string
) => {
    const baseUrl = import.meta.env.VITE_BACKEND_API_URL_PREFIX || 'http://127.0.0.1:8000';
    let body: string | undefined;

    let _url = baseUrl + url;

    if (method === 'GET') {
        const urlParams = new URLSearchParams(params).toString();
        _url += `?${urlParams}`;
    } else {
        body = JSON.stringify(params);
    }

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options: RequestInit = {
        method,
        headers,
        body: method !== 'GET' ? body : undefined,
    };

    fetch(_url, options)
        .then(async response => {
            const json = await response.json();
            if (response.ok) {
                if (successCallback) {
                    successCallback(json);
                }
            } else {
                if (failureCallback) {
                    failureCallback(json);
                } else {
                    alert(JSON.stringify(json));
                }
            }
        })
        .catch(error => {
            alert(JSON.stringify(error));
        });
};

export default fastapi;
