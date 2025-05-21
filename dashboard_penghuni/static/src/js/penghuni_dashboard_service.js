import { PenghuniDashboard } from './penghuni_dashboard';

odoo.define('dashboard_penghuni.PenghuniDashboard', function (require) {
    const { Component } = require('web.core');
    const { mount } = owl;

    mount(PenghuniDashboard, { env: { services: odoo.services } }, document.querySelector('.penghuni-dashboard-template'));
});