# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpSerialNumber(models.Model):
	_name = 'mrp.serial.number'
	_description = 'Request Part for BoM'
	_order = 'date_scheduled desc'

	name = fields.Char(copy=False,  index=True, default=lambda self: _('New'))
	sale_id = fields.Many2one('sale.order', string='SO Reference')
	product_id = fields.Many2one('product.template', string="Product", )
	partner_id = fields.Many2one('res.partner', string="Customer", related='sale_id.partner_id')
	bom_id = fields.Many2one('mrp.bom', string="Bill of Materials")
	location_src_id = fields.Many2one('stock.location', string="Source Location", domain=[('usage', '=', 'internal')])
	location_dest_id = fields.Many2one('stock.location', string="Destination Location", domain=[('usage', '=', 'internal')])
	date_scheduled = fields.Datetime(string="Scheduled Date")
	part_request_ids = fields.One2many('mrp.part.request.line', 'part_request_id', string="Material Request Line")
	warehouse_id = fields.Many2one('stock.warehouse', string="User")
	picking_count = fields.Integer(compute="compute_picking_count")
	production_id = fields.Many2one('mrp.production', string="Production")
	company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, readonly=True, default=lambda self: self.env.user.company_id.id)
	user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
	categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, domain="[('type','=','normal')]",
        required=True, help="Select category for the current product", related='product_id.categ_id')
	date = fields.Date(string='Tanggal',default=fields.Date.today())
	manufacturing_id = fields.Many2one('mrp.production', string='MO Reference')
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
	def default_get(self, fields):
		res = super(MrpSerialNumber, self).default_get(fields)
		warehouse_obj = self.env['stock.warehouse']
		warehouse = warehouse_obj.search([('id', '=', 1)], limit=1)
		if warehouse:
			res['warehouse_id'] = warehouse.id
			res['location_src_id'] = warehouse.lot_stock_id.id
		return res

	@api.multi
	@api.onchange('production_id', 'production_id.partner_id', 
		'production_id.bom_id', 'production_id.product_id')
	def onchange_production_id(self):
		for doc in self:
			if doc.production_id:
				prod_id = doc.production_id
				doc.partner_id = prod_id.partner_id and prod_id.partner_id.id or False
				doc.bom_id = prod_id.bom_id.id
				doc.product_id = prod_id.product_id.product_tmpl_id.id

	@api.multi
	@api.onchange('product_id')
	def onchange_product_template(self):
		for doc in self:
			product = doc.product_id
			if product:
				bom_ids = product.bom_ids.filtered(lambda x: x.active == True)
				if any(bom_ids):
					doc.bom_id = bom_ids[0].id

	@api.multi
	@api.onchange('warehouse_id')
	def onchange_warehouse_id(self):
		for doc in self:
			wh = doc.warehouse_id
			if wh:
				doc.location_src_id = wh.lot_stock_id.id

	@api.multi
	def action_confirm(self):
		picking_type_obj = self.env['stock.picking.type']
		for req in self:
			src_loc = req.location_src_id
			dst_loc = req.location_dest_id
			domain = [('warehouse_id', '=', req.warehouse_id.id), 
						('code', '=', 'internal')]
			picking_type = picking_type_obj.search(domain, limit=1)
			values = {
				'location_id': src_loc.id,
				'location_dest_id': dst_loc.id,
				'min_date': req.date_scheduled,
				'origin': req.name,
				'picking_type_id': picking_type.id,
				'request_material_id': req.id
			}
			picking = self.env['stock.picking'].create(values)
			for line in req.part_request_ids:
				vals = {
					'product_id': line.product_id.id,
					'name': line.product_id.display_name,
					'product_uom_qty': line.quantity,
					'product_uom': line.uom_id.id,
					'location_id': src_loc.id,
					'location_dest_id': dst_loc.id,
				}
				move = self.env['stock.move'].create(vals)
				if move:
					picking.write({'move_lines': [(4, move.id)]})
					line.write({'move_id': move.id})
			picking.action_confirm()
			picking.action_assign()
		self.write({'state': 'confirm'})

	@api.multi
	def compute_picking_count(self):
		for req in self:
			moves = req.part_request_ids.mapped('move_id')
			picks = moves.mapped('picking_id')
			req.picking_count = len(picks)
	
	# @api.model
    # def create(self, vals):
    #     seq = self.env['ir.sequence'].get('mrp.serial.number') 
    #     vals['name'] = seq
    #     result = super(MrpSerialNumber,self).create(vals)
    #     return result


	@api.model
	def create(self, vals):
		# if not vals.get('name', False) or vals['name'] == _('New'):
		# 	vals['name'] = self.env['ir.sequence'].next_by_code('mrp.serial.number') or _('New')
		# res = super(MrpSerialNumber, self).create(vals)
		if vals.get('bom_id') or vals.get('production_id'):
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
		elif vals.get('product_selection') == 'floorstand43':
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
		res = super(MrpSerialNumber, self).create(vals)
		res.action_fill_part_request_lines()
		return res


	@api.multi
	def action_fill_part_request_lines(self):
		for req in self:
			part_line_obj = self.env['mrp.part.request.line']
			moves_todo = self.env['stock.move']
			new_line_ids = []
			if req.production_id:
				# if have MO
				moves = req.production_id.move_raw_ids
				moves_todo = moves.filtered(lambda x: x.state in ['draft', 'waiting', 'confirmed'])
				bom_lines = req.bom_id and req.bom_id.bom_line_ids or self.env['mrp.bom.line']
				for move in moves_todo:
					line = bom_lines.filtered(lambda l: l.product_id.id == move.product_id.id)
					qty = (move.product_uom_qty - move.reserved_availability)
					vals = {
						'product_id': move.product_id.id,
						'description': move.product_id.display_name,
						'uom_id': move.product_uom.id,
						'quantity': qty,
						'item_size': line and line.item_size or False,
						'item_qty': line and line.item_qty or 0
					}
					new_line = part_line_obj.create(vals)
					new_line_ids.append(new_line.id)
			elif not req.production_id and req.bom_id:
				# If don't MO but have Bill of Materials
				for line in req.bom_id.bom_line_ids:
					vals = {
						'product_id': line.product_id.id,
						'description': line.product_id.display_name,
						'uom_id': line.product_uom_id.id,
						'quantity': line.product_qty,
						'item_size': line.item_size,
						'item_qty': line.item_qty
					}
					new_line = part_line_obj.create(vals)
					new_line_ids.append(new_line.id)
			if new_line_ids:
				req.write({'part_request_ids': [(6, 0, new_line_ids)]}) 
		return True
	
	@api.multi
	def write(self, vals):
		res = super(MrpSerialNumber, self).write(vals)
		if 'bom_id' in vals or 'production_id' in vals:
			self.action_fill_part_request_lines()
		return res

	@api.multi
	def action_view_picking(self):
		moves = self.mapped('part_request_ids').mapped('move_id')
		pickings = moves.mapped('picking_id')
		action = self.env.ref('stock.action_picking_tree_all').read()[0]
		if len(pickings) > 1:
			action['domain'] = [('id', 'in', pickings.ids)]
		elif len(pickings) == 1:
			action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
			action['res_id'] = pickings.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		action['context'] = self.env.context
		return action

	def get_line_per10(self):
		""" Limit line per Page on Report """
		res = []
		all_line = self.part_request_ids
		total_page = len(all_line) // 10
		if len(all_line) % 10 != 0:
			total_page += 1
		index_slice = 0
		res_append = res.append
		for x in range(total_page):
			res_append(all_line[index_slice:index_slice + 10])
			index_slice += 10
		return res

	def get_picking(self):
		""" Get Picking for Report """
		moves = self.part_request_ids.mapped('move_id')
		picking = moves.mapped('picking_id')
		if picking:
			return picking[0].name

	def get_department(self):
		""" Get Department for Report """
		if self.user_id:
			emp = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
			if emp and emp.department_id:
				return emp.department_id.name

	# @api.multi
	# def unlink(self):
	# 	for req in self:
	# 		if req.state != 'draft':
	# 			raise UserError(_("You can not delete Material Request that not in Draft."))
	# 	return super(MrpSerialNumber, self).unlink()


class MrpPartRequestLine(models.Model):
	_name = 'mrp.part.request.line'

	part_request_id = fields.Many2one('mrp.serial.number', string="Material Request")
	sale_id = fields.Many2one('sale.order', string='SO Reference')	
	product_id = fields.Many2one('product.product', string="Product")
	description = fields.Char()
	serial_number_ids = fields.Many2many('serial.number.pabrik',string='Serial Number Pabrik')
	serial_number_pabrik = fields.Char(string = 'Serial Number Pabrik',)
	quantity = fields.Float()
	uom_id = fields.Many2one('product.uom', string="Unit of Measure")
	item_size = fields.Char()
	item_qty = fields.Integer()
	move_id = fields.Many2one('stock.move', string="Stock Move")
	

	@api.multi
	@api.onchange('product_id')
	def onchange_product_id(self):
		for line in self:
			line.uom_id = line.product_id and line.product_id.uom_id.id or False
