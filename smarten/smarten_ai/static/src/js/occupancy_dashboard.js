odoo.define('smarten_ai.occupancy_dashboard', function (require) {
    "use strict";
    var KanbanView = require('web.KanbanView');

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

    // Do NOT add to viewRegistry – js_class="occupancy_dashboard" in XML handles it
});