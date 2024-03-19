import ajax from '../utils/ajax';
import router from '../router/router';
import store from '../store/store';
//import cache from '../utils/cache';
//import { getCacheKey } from '../utils/helpers';

class RESTError extends Error {
    constructor(error, message, params={}) {
        let detail = error.response && error.response.data && (error.response.data.detail || error.response.data.error && error.response.data.error.detail);
        let header = (message || error.message) + (detail ? ': ' + detail : '');
        super(header);

        this.name = this.constructor.name;
        this.parent = error;
        this.detail = detail;
        this.response = error.response;
        for (let k in params) {
            this[k] = params[k];
        }

        if (typeof Error.captureStackTrace === 'function') {
            Error.captureStackTrace(this, this.constructor);
        } else { 
            this.stack = (new Error(header)).stack; 
        }

        if (this.response && this.response.status === 401) {
            store.dispatch('clearUser');
            store.dispatch('clearToken');
            //store.dispatch('showError', 'Доступ запрещен!');
            router.push({ name: 'home' });
        }
    }
}

class REST {
    static get settings() {
        throw new Error('settings must be overridden');
    }
    //static get serviceName() {
    //    throw new Error('serviceName must be overridden');
    //}
    static _get(url, params={}, use_cache=false) {
        return this._request('get', url, params, {}, use_cache);
    }
    static _post(url, params, data) {
        return this._request('post', url, params, data);
    }
    static _put(url, params, data) {
        return this._request('put', url, params, data);
    }
    static _patch(url, params, data) {
        return this._request('patch', url, params, data);
    }
    static _delete(url, params, data) {
        return this._request('delete', url, params, data);
    }
    static _request(method, url, params={}, data={}, use_cache=false) {
        //let cache_key = null;
        if (use_cache) {
        //    cache_key = getCacheKey(this.serviceName, ajax.getUri({ url, params }), data);
        //    const result = cache.get(cache_key);
        //    if (result) {
        //        return Promise.resolve(result);
        //    }
        }
        // console.log(params, data);
        return ajax.request({
            method,
            url: `${this.settings.url}/${url}/`,
            params,
            data,
            headers: this._getAuthHeaders()
        }).then((response) => {
            //if (cache_key) {
            //    cache.set(cache_key, response.data);
            //}
            return response.data;
        });
    }
    static _getAuthHeaders() {
        //return { 'Authorization': `Token ${this.settings.token}` };
        //console.log('Token:', store.state.access);
        if (store.state.access) {
            return { 'Authorization': `Bearer ${store.state.access}` };
        } else {
            return {};
        }
    }
}

export default REST;

export {
    RESTError,
    REST
};
