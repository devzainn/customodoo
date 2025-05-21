odoo.define('testing_challenge_tree.on_tree_click', function(require) {
    "use strict";
  
    var core = require('web.core');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var rpc = require('web.rpc'); // Import the RPC module
  
    ListView.include({
      render: function () {
        this._super.apply(this, arguments);
  
        // Add click event listener to each row in the tree view
        var self = this;
        this.$el.find('.o_data_row').on('click', function(event) {
          var recordID = $(this).data('id');
          if (recordID) {
            self._renderFormView(recordID); // Call function to render the form below the tree
          }
        });
      },
  
      // Custom function to render the form view inline below the tree
      _renderFormView: function(recordID) {
        var self = this;
  
        // Clear any previously rendered form view to avoid duplicates
        this.$el.find('.o_form_container').remove();
  
        // RPC call to fetch the data for the selected record
        rpc.query({
          model: 'testing.challenge.tree',
          method: 'read',
          args: [[recordID]],
        }).then(function(data) {
          if (data && data.length) { // Check if data is not empty
            console.log("Data fetched for record ID:", recordID);
  
            // Render the form view in readonly mode
            var formView = new FormView(self, {
              model: 'testing.challenge.tree',
              id: recordID,
              mode: 'readonly', // Read-only mode
            });
  
            // Append the form view below the tree
            var $formContainer = $('<div class="o_form_container"></div>');
            self.$el.append($formContainer); // Append to the current tree view
            formView.appendTo($formContainer).then(function() {
              formView.do_show();
              formView.do_load_record(data[0]);
            });
          } else {
            console.log("No data returned for record ID:", recordID);
          }
        }).catch(function(error) {
          console.error("Error fetching data:", error);
        });
      }
    });
  });
  