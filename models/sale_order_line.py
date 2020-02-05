from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _name = 'sale.order.line'
     
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    # product_id = fields.Many2one('product.product', string='Product', related='sale_ids.product_id', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    name = fields.Text(string='Description', required=True)
    qty_id = fields.Integer(string="Order Qty", required=True, default='1')
    no_serial = fields.Char (string="No Serial Number", required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    
    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        result = {'domain': domain}

        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
                return result

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        return result