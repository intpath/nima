# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
	_inherit = "stock.move"

	product_uom_to = fields.Many2one('uom.uom', string='UoM To', domain="[('category_id', '=', product_uom_category_id)]")
	product_qty_to = fields.Float(string='Quantity To', compute = "_compute_product_qty_to")

	@api.model
	def create(self, values):
		if values.get('purchase_line_id'):
			purchase_line_id  = self.env['purchase.order.line'].browse( values['purchase_line_id'] )
			purchase_product_id = purchase_line_id.product_id
			found_bom_kit = self.env["mrp.bom"].search([("product_tmpl_id", "=", purchase_product_id.product_tmpl_id.id), ("type", "=", "phantom")])
			if len(found_bom_kit) == 0:
				values['product_uom'] = purchase_line_id.product_uom.id
				values['product_uom_qty'] = purchase_line_id.product_qty
		
		res = super(StockMove, self).create(values)
		return res


	@api.onchange('product_uom_to')
	def _compute_product_qty_to(self):
		for rec in self:
			if rec.product_uom_to:

				if rec.product_uom_to.uom_type == 'bigger':
					rec.product_qty_to = rec.product_qty / rec.product_uom_to.factor_inv
				elif rec.product_uom_to.uom_type == 'smaller':
					rec.product_qty_to = rec.product_qty * rec.product_uom_to.factor_inv
				elif rec.product_uom_to.uom_type == 'reference':
					rec.product_qty_to = rec.product_qty
			else:
				rec.product_qty_to = False
