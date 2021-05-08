odoo.define('my_module.MyCustomForm', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var viewRegistry = require('web.view_registry');
    var FormView = require('web.FormView');

    var MyFormController = FormController.extend({
        _updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                if ((this.renderer.state.data.state !== 'waiting_for_approval') &&
                    (this.renderer.state.data.state !== 'approved')) {
                    this.$buttons.find('.o_form_button_edit').show();
                } else {
                    this.$buttons.find('.o_form_button_edit').hide();
                }
            }
        },
    });

    var MyFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: MyFormController,
        }),
    });
    viewRegistry.add('custom_form', MyFormView);

});

