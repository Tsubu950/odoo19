/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { registry } from "@web/core/registry";

class SmartenRawKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.reloadInterval = setInterval(() => {
            this.model.load();
        }, 5000); // refresh every 5 seconds
    }
    destroy() {
        clearInterval(this.reloadInterval);
        super.destroy();
    }
}
SmartenRawKanbanRenderer.template = "smarten_raw_log.KanbanRenderer";

registry.category("kanban_renderers").add("smarten_raw_kanban", SmartenRawKanbanRenderer);