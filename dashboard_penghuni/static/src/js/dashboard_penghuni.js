import { Component, useState } from '@odoo/owl';

export class PenghuniDashboard extends Component {
    static template = "PenghuniDashboardTemplate";

    setup() {
        this.state = useState({
            kodeRumahFilter: "",
            startDate: "",
            endDate: "",
            produkPengeluaran: {},
            produkUsage: {},
            paymentHistory: [],
            activeTagihan: [],
            paidTagihan: [],
        });

        this.loadDashboardData();
    }

    async loadDashboardData() {
        const response = await this.env.services.rpc("/penghuni_dashboard/get_data", {});
        this.state.produkPengeluaran = response.produk_pengeluaran;
        this.state.produkUsage = response.produk_usage;
        this.state.paymentHistory = response.payment_history;
        this.state.activeTagihan = response.active_tagihan;
        this.state.paidTagihan = response.paid_tagihan;
    }

    applyFilter() {
        console.log("Apply Filter", this.state);
        this.loadDashboardData(); 
    }
}
