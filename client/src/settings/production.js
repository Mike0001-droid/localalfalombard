const ajax = {
    timeout: 45000,
    responseType: 'json',
    responseEncoding: 'utf8'
};

const serviceUrl = {
    url: '//lk.permlom.ru',
    localPath: '//lk.permlom.ru',
    protocol: 'https',
    port: '80',
    api: '/api',
    onLocal: false
}

let urlPath = `${serviceUrl.url}${serviceUrl.api}`;
if (serviceUrl.onLocal || window.location.hostname === 'localhost') {
    urlPath = `${serviceUrl.localPath}:${serviceUrl.port}${serviceUrl.api}`;
}

let servicePath = `${serviceUrl.protocol}:${window.location.hostname === 'localhost' ? 
                serviceUrl.localPath + ':' + serviceUrl.port : serviceUrl.url }`

const app = {
    url: `${urlPath}`,
    token: 'd53d94913abf172aed172eb875bf546fcfdd5cef'
};

const cache = {
    storage: 'sessionStorage'
};

const logger = {
    url: `${urlPath}/logger`,
    level: 'debug',
    token: 'd53d94913abf172aed172eb875bf546fcfdd5cef'
};

export {
    ajax,
    app,
    cache,

    logger,

    servicePath
};