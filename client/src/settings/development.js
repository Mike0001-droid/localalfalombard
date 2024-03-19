const ajax = {
    timeout: 75000,
    responseType: 'json',
    responseEncoding: 'utf8'
};

const serviceUrl = {
    url: '//lombard.flexidev.ru',
    localPath: '//localhost',
    protocol: 'http',
    port: '8000',
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
    token: 'c7d63a2e58d186ae3760a5f7c690293e973c08c4'
};

const cache = {
    storage: 'sessionStorage'
};

const logger = {
    url: `${urlPath}/logger`,
    level: 'debug',
    token: 'c7d63a2e58d186ae3760a5f7c690293e973c08c4'
};

export {
    ajax,
    app,
    cache,

    logger,

    servicePath
};