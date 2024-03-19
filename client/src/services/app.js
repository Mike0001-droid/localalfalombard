import { app as settings } from '@/settings';
import { REST, RESTError } from './rest';

export default class extends REST {
    static get settings() {
        return settings;
    }

    static obtainToken(params) {
        return this._post(`user/token/create`, {}, params).then((data) => {
            let tokens = data;
            return tokens;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось авторизоваться');
        });
    }

    static refreshToken(token) {
        return this._post(`user/token/refresh`, {}, { refresh: token }).then((data) => {
            let tokens = data;
            return tokens;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось обновит токен');
        });
    }

    static createUser(params) {
        return this._post(`user/create_user`, {}, params).then((data) => {
            let tokens = data;
            return tokens;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось создать пользователя');
        });
    }

    static updateUser(params) {
        return this._post(`user/update_user`, {}, params).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось обновить данные пользователя');
        });
    }

    static checkUser(params) {
        return this._post(`user/check_user`, {}, params).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось проверить пользователя');
        });
    }

    static getProfile() {
        return this._get(`user/profile`, {}, {}).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить пользователя');
        });
    }

    static resetPassword(params) {
        return this._post(`user/password_reset_user`, {}, params).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось сбросить пароль пользователя');
        });
    }

    static updatePassword(params) {
        return this._post(`user/update_password`, {}, params).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось сбросить пароль пользователя');
        });
    }

    static askQuestion(params) {
        return this._post(`user/ask_question`, {}, params).then((data) => {
            let user = data;
            return user;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось отправить вопрос');
        });
    }

    static getSiteInfo() {
        return this._get(`user/get_site_info`, {}, {}).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить общую информацию');
        });
    }

    // Метод не реализован в 1С
    static getTicketsSum(params) {
        return this._post(`lombard/get_tickets_sum`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить общей информации');
        });
    }

    static getTickets(params) {
        return this._post(`lombard/get_tickets`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить залоговые билеты');
        });
    }

    static getTicket(params) {
        return this._post(`lombard/get_ticket_info`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить залоговый билет');
        });
    }

    static getTicketDebt(params) {
        return this._post(`lombard/get_debt`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить информации по сумме процентов');
        });
    }

    static getTicketAccrual(params) {
        return this._post(`lombard/get_ticket_accrual`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить информации по начислению процентов');
        });
    }

    static setTicketFavorite(params) {
        return this._post(`lombard/favorites/pin`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось изменить статус залогового билета');
        });
    }

    static unsetTicketFavorite(params) {
        return this._post(`lombard/favorites/unpin`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось изменить статус залогового билета');
        });
    }

    static getTicketsFavorite(params) {
        return this._post(`lombard/favorites`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить избранные залоговые билеты');
        });
    }

    static getPage(slug) {
        return this._get(`lombard/pages/${slug}`, {}, {}).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось получить страницу');
        });
    }

    static payTicket(params) {
        return this._post(`payments/pay`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось произвести оплату');
        });
    }

    static payTicketAlt(params) {
        return this._post(`payments/pay_aft`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось произвести оплату');
        });
    }

    static payTicketResult(params) {
        return this._post(`payments/result`, {}, params).then((data) => {
            let info = data;
            return info;
        }).catch((error) => {
            throw new RESTError(error, 'Не удалось произвести проверку платежа');
        });
    }
}
