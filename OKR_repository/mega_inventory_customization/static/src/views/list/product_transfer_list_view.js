/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useService } from "@web/core/utils/hooks";

//add new button in product transfer tree view
export class ProductTransferController extends ListController {
   setup() {
       super.setup();
       this.orm = useService("orm");
   }
  // called action_all_transfer method to transfer all product
   async OnTransferClick() {
       await this.orm.call(
            "product.transfer",
            "action_all_transfer",[this.id]
        );
        document.location.reload();
   }
}
registry.category("views").add("product_transfer", {
   ...listView,
   Controller: ProductTransferController,
   buttonTemplate: "button_product_transfer.ListView.Buttons",
});
