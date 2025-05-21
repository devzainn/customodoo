odoo.define('testing_challenge_tree.tree_detail', function (require) {
    'use strict';

    var ListView = require('web.ListView');
    var core = require('web.core');
    var QWeb = core.qweb;

    ListView.include({
        init: function (parent, options) {
            this._super(parent, options);
            this.clicked_record = null; 
        },


        _onRowClicked: function (event) {
            var $row = $(event.currentTarget);
            var record_id = $row.data('id'); 

            if (this.clicked_record === record_id) {
                this.clicked_record = null;
                this.$el.find('.tree_detail').remove(); 
            } else {
                this.clicked_record = record_id;

                var self = this;
                this._rpc({
                    model: 'testing.challenge.tree',
                    method: 'read',
                    args: [[record_id], ['name', 'kebutuhan_uan']],  
                }).then(function (data) {
                    var $detail = $('<tr class="tree_detail"><td colspan="4">' +
                        '<div class="o_detail_form">' +
                        '<strong>Name:</strong> ' + data[0].name + '<br>' +
                        '<strong>Kebutuhan Uang:</strong> ' + data[0].kebutuhan_uan +
                        '</div></td></tr>');

                    $row.after($detail);
                });
            }
        },

        render_buttons: function ($node) {
            this._super($node);
            var self = this;

            this.$('.o_data_row').on('click', function (event) {
                self._onRowClicked(event);
            });
        },
    });
});
