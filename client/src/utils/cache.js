import _keys from 'lodash/keys';
import { cache as settings } from '@/settings';

class Converter {
    static encode(value) {
        return this.__isComplex(value) ? JSON.stringify(value) : value;
    }
    static decode(value) {
        return this.__isJSON(value) ? JSON.parse(value) : value;
    }
    static __isComplex(value) {
        return (value instanceof Array || typeof value === 'object');
    }
    static __isJSON(value) {
        return (typeof value === 'string' && /^(\{|\[)/.test(value));
    }
}


class TempStorage {
    constructor() {
        this.__data = {};
    }
    getItem(key) {
        return this.__data[key];
    }
    setItem(key, value) {
        this.__data[key] = value;
    }
    removeItem(key) {
        delete this.__data[key];
    }
    clear() {
        this.__data = {};
    }
    get length() {
        return _keys(this.__data).length;
    }
}


class Cache {
    constructor(storage) {
        if (storage === 'tempStorage') {
            this._storage = new TempStorage();
        } else {
            if (!(storage in window)) {
                throw new Error(`Storage ${storage} is not supported`);
            }
            this._storage = window[storage];
        }
    }
    get(key) {
        return Converter.decode(this._storage.getItem(key));
    }
    set(key, value) {
        this._storage.setItem(key, Converter.encode(value));
    }
    remove(key) {
        this._storage.removeItem(key);
    }
    clear() {
        this._storage.clear();
    }
}


export default new Cache(settings.storage);
