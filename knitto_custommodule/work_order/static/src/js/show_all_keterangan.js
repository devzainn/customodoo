odoo.define('show_all_keterangan', function (require) {
    "use strict";

    let core = require('web.core');
    let ListView = require('web.ListView');

    let ShowAllKeteranganView = ListView.extend({
        render_buttons: function () {
            this._super.apply(this, arguments);
            let self = this;

            // Event handler untuk tombol
            this.$el.find('.show_all_keterangan_btn').on('click', function () {
                self._onShowAllKeteranganClick();
            });

            this.$el.find('.show_all_note_btn').on('click', function () {
                self._onShowAllNoteClick();
            });
        },

        _onShowAllKeteranganClick: function () {
            console.log("Button 'Tampilkan Semua Keterangan' diklik.");
            this._fetchAndDisplayKeterangan();
        },

        _onShowAllNoteClick: function () {
            console.log("Button 'Tampilkan Semua Note' diklik.");
            this._fetchAndDisplayNote();
        },

        _fetchAndDisplayKeterangan: function () {
            let self = this;
            this.dataset.read_slice(['name', 'keterangan']).then(function (records) {
                let keteranganList = records.map(record => record.keterangan).join('\n');
                alert("Semua Keterangan:\n" + keteranganList);
            });
        },

        _fetchAndDisplayNote: function () {
            let self = this;
            this.dataset.read_slice(['name', 'note']).then(function (records) {
                let noteList = records.map(record => record.note).join('\n');
                alert("Semua Note:\n" + noteList);
            });
        }
    });

    core.view_registry.add('show_all_keterangan_view', ShowAllKeteranganView);
    return ShowAllKeteranganView;
});
