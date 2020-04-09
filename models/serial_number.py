from odoo import api, models, fields, models, _
from datetime import datetime,timedelta,time

class SerialNumber(models.Model):
    _name = "serial.number"
    _description = "Serial Number"

    name = fields.Char(string='Serial Number',  copy=False,  index=True, default=lambda self: _('New'))
    sale_id = fields.Many2one('sale.order', string='SO Reference')
    partner_id = fields.Many2one('res.partner',string='Customer', track_visibility='onchange', related='sale_id.partner_id')
    date = fields.Date(string='Tanggal',default=fields.Date.today())
    qty_id = fields.Integer(string="Qty", required=True, default='1')
    serial_number_note = fields.Text(string='Note')
    product_id = fields.Many2one('product.product', string='Product', related='sale_id.product_id', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, domain="[('type','=','normal')]",
        required=True, help="Select category for the current product", related='product_id.categ_id')
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', copy=True)
    product_selection = fields.Selection(
        selection=[
            ('floorstand43', 'Digital AD Display Floorstand 43"'),
            ('floorstand49', 'Digital AD Display Floorstand 49"'),
            ('floorstand55', 'Digital AD Display Floorstand 55"'),
            ('digisig43', 'Dual Side Digital Signage 43 Inch'),
            ('digisig55', 'Dual Side Digital Signage 55 Inch'),
            ('eduplay32b', 'EduPlay Table 32 Inch - Blue'),
            ('eduplay32r', 'EduPlay Table 32 Inch - Red'),
            ('kiosk21.5', 'Interactive Android Kiosk 21.5"'),
            ('kiosk27', 'Interactive Android Kiosk 27"'),
            ('kiosk32', 'Interactive Android Kiosk 32"'),
            ('display22', 'LCD AD DISPLAY 22"'),
            ('display32', 'LCD AD DISPLAY 32"'),
            ('touchfloorstand49', 'Monitor Touchscreen Floorstand 49"'),
            ('touchfloorstand55', 'Monitor Touchscreen Floorstand 55"'),
            ('touchmonitor32', 'TOUCH SCREEN MONITOR 32" (W320RM)'),
            ('touchmonitor43', 'TOUCH SCREEN MONITOR 43" (W430RM)'),
            ('touchmonitor49', 'TOUCH SCREEN MONITOR 49" (W490RM)'),
            ('touchmonitor55', 'TOUCH SCREEN MONITOR 55" (W550RM)'),
            ('adigisig32', 'A-Digital Signage 32 Inch'),
            ('adigisig43', 'A-Digital Signage 43 Inch'),
            ('adigisig43touch', 'A-Digital Signage Touchscreen 43 Inch'),
            ('interactivecontroller', 'INTERACTIVE CONTROLLER BOX'),
            ('addisplay', 'AD Display Controller Box'),
            ('ice265', 'ICE Board 65 Inch 4K UHD - Version II '),
            ('ice275', 'ICE Board 75 Inch 4K UHD - Version II '),
            ('ice286', 'ICE Board 86 Inch 4K UHD - Version II '),
            ('ice298', 'ICE Board 98 Inch 4K UHD - Version II '),
            ('ops', 'OPS 4K PC Module with Windows 10 IOT'),
            ('opsi5vpro', 'OPS 4K PC Intel i5 VPro with Windows 10 IOT'),
            ('wsk', 'Wireless Screenshare Kit'),
            ('VSOKAC32', 'Self Order Kiosk Platform Android 32" Capacitive Touch'),
            ('VSOKAC43', 'Self Order Kiosk Platform Android 43" Capacitive Touch'),
            ('VSOKAR32', 'Self Order Kiosk Platform Android 32" IR touch'),
            ('VSOKAR43', 'Self Order Kiosk Platform Android 43" IR touch'),
            ('VSOKIC32', 'Self Order Kiosk Platform Intel I3 with Windows 10 IOT 32" Capacitive Touch'),
            ('VSOKIC43', 'Self Order Kiosk Platform Intel I3 with Windows 10 IOT 43" Capacitive Touch'),
            ('VSOKIR32', 'Self Order Kiosk Platform Intel I3 with Windows 10 IOT 32" IR Touch'),
            ('VSOKIR43', 'Self Order Kiosk Platform Intel I3 with Windows 10 IOT 43" IR Touch'),
            ('VSSKA215', 'Self Services Kiosk Basic - Platform Android 21.5" touch'),
            ('VSSKI215', 'Self Services Kiosk Basic - Platform Intel I3 with Windows 10 IOT 21.5" touch'),
            ('qdsp5', 'Controller QDSP Box i5'),
            ],
        string='Product Name')
    
    @api.model
    def create(self,vals):
		if vals.get('product_selection') == 'floorstand43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.floorstand43')
		elif vals.get('product_selection') == 'floorstand49':
			vals['name'] = self.env['ir.sequence'].get('serial.number.floorstand49')
		elif vals.get('product_selection') == 'floorstand55':
			vals['name'] = self.env['ir.sequence'].get('serial.number.floorstand55')
		elif vals.get('product_selection') == 'digisig43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.digisig43')
		elif vals.get('product_selection') == 'digisig55':
			vals['name'] = self.env['ir.sequence'].get('serial.number.digisig55')
		elif vals.get('product_selection') == 'eduplay32b':
			vals['name'] = self.env['ir.sequence'].get('serial.number.eduplay32b')
		elif vals.get('product_selection') == 'eduplay32r':
			vals['name'] = self.env['ir.sequence'].get('serial.number.eduplay32r')
		elif vals.get('product_selection') == 'kiosk21.5':
			vals['name'] = self.env['ir.sequence'].get('serial.number.kiosk21.5')
		elif vals.get('product_selection') == 'kiosk27':
			vals['name'] = self.env['ir.sequence'].get('serial.number.kiosk27')
		elif vals.get('product_selection') == 'kiosk32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.kiosk32')
		elif vals.get('product_selection') == 'display22':
			vals['name'] = self.env['ir.sequence'].get('serial.number.display22')
		elif vals.get('product_selection') == 'display32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.display32')
		elif vals.get('product_selection') == 'touchfloorstand49':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchfloorstand49')
		elif vals.get('product_selection') == 'touchfloorstand55':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchfloorstand55')
		elif vals.get('product_selection') == 'touchmonitor32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchmonitor32')
		elif vals.get('product_selection') == 'touchmonitor43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchmonitor43')
		elif vals.get('product_selection') == 'touchmonitor49':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchmonitor49')
		elif vals.get('product_selection') == 'touchmonitor55':
			vals['name'] = self.env['ir.sequence'].get('serial.number.touchmonitor55')
		elif vals.get('product_selection') == 'adigisig32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.adigisig32')
		elif vals.get('product_selection') == 'adigisig43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.adigisig43')
		elif vals.get('product_selection') == 'adigisig43touch':
			vals['name'] = self.env['ir.sequence'].get('serial.number.adigisig43touch')
		elif vals.get('product_selection') == 'interactivecontroller':
			vals['name'] = self.env['ir.sequence'].get('serial.number.interactivecontroller')
		elif vals.get('product_selection') == 'addisplay':
			vals['name'] = self.env['ir.sequence'].get('serial.number.addisplay')
		elif vals.get('product_selection') == 'ice265':
			vals['name'] = self.env['ir.sequence'].get('serial.number.ice265')
		elif vals.get('product_selection') == 'ice275':
			vals['name'] = self.env['ir.sequence'].get('serial.number.ice275')
		elif vals.get('product_selection') == 'ice286':
			vals['name'] = self.env['ir.sequence'].get('serial.number.ice286')
		elif vals.get('product_selection') == 'ice298':
			vals['name'] = self.env['ir.sequence'].get('serial.number.ice298')
		elif vals.get('product_selection') == 'ops':
			vals['name'] = self.env['ir.sequence'].get('serial.number.ops')
		elif vals.get('product_selection') == 'opsi5vpro':
			vals['name'] = self.env['ir.sequence'].get('serial.number.opsi5vpro')
		elif vals.get('product_selection') == 'wsk':
			vals['name'] = self.env['ir.sequence'].get('serial.number.wsk')
		elif vals.get('product_selection') == 'VSOKAC32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKAC32')
		elif vals.get('product_selection') == 'VSOKAC43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKAC43')
		elif vals.get('product_selection') == 'VSOKAR32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKAR32')
		elif vals.get('product_selection') == 'VSOKAR43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKAR43')
		elif vals.get('product_selection') == 'VSOKIC32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKIC32')
		elif vals.get('product_selection') == 'VSOKIC43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKIC43')
		elif vals.get('product_selection') == 'VSOKIR32':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKIR32')
		elif vals.get('product_selection') == 'VSOKIR43':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSOKIR43')
		elif vals.get('product_selection') == 'VSSKA215':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSSKA215')
		elif vals.get('product_selection') == 'VSSKI215':
			vals['name'] = self.env['ir.sequence'].get('serial.number.VSSKI215')
		elif vals.get('product_selection') == 'qdsp5':
			vals['name'] = self.env['ir.sequence'].get('serial.number.qdsp5')
		else:
			vals['name'] = self.env['ir.sequence'].get('serial.number')
		res = super(SerialNumber, self).create(vals)
		return res