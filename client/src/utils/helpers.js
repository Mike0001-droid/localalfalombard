//import _keys from 'lodash/keys';
import { parse, format } from 'fecha';


const helpers = {
    parseDate: (value, template) => {
        return parse(value, template);
    },

    formatDate: (value, template) => {
        return format(value, template);
    },

    stringForNumber: (value, strings) => {
        let idx = 2;
        let num = value;
        if (num > 100) {
            num = num % 100;
        }
        if ((num < 10) || (num > 19)) {
            let z = num % 10;
            if (z === 1) {
                idx = 0;
            } else if ((z > 1) && (z < 5)) {
                idx = 1;
            }
        }
        return value + ' ' + strings[idx];
    },

    toPrice: (value, params) => {
        if (!params) {
            params = {};
        }
        value = value * 1;
        let kop = Math.floor((Math.abs(value - Math.floor(value)) + 0.005) * 100);
        if (kop < 10) {
            kop = '0' + kop;
        }
        value = Math.floor(value + 0.0001);
        value = value + '';
        let text = '';
        let l = value.length;
        let i = 0;
        let k;
        while (i < l) {
            k = ((i === 0) && (l % 3 > 0)) ? l % 3 : 3;
            if (i + k < l) {
                text = text + value.substr(i, k) + ' ';
            } else {
                text = text + value.substr(i, k);
            }
            i = i + k;
        }
        if (params.pointer) {
            text = text + params.pointer + kop;
        }
        if (params.sign) {
            text = text + ' ' + params.sign;
        }
        return text;
    },

    validateEmail: (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
             );
    }
}

export default {
    install (app) {
        app.helpers = helpers
        app.config.globalProperties.$helpers = helpers
    }
}
