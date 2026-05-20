odoo.define('smarten_ai.occupancy_dashboard', function (require) {
    "use strict";
    var KanbanView = require('web.KanbanView');
    var viewRegistry = require('web.view_registry');

    var OccupancyKanban = KanbanView.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.interval = setInterval(this._reload.bind(this), 5000);
        },
        _reload: function () {
            this.reload();
        },
        destroy: function () {
            if (this.interval) clearInterval(this.interval);
            this._super.apply(this, arguments);
        }
    });
    viewRegistry.add('occupancy_dashboard', OccupancyKanban);
});