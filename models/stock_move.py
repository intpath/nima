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


	@api.onchange('product_uom_to', 'product_qty')
	def _compute_product_qty_to(self):
		for rec in self:
			if rec.product_uom_to:

				if rec.product_uom_to.uom_type == 'bigger':
					rec.product_qty_to = (rec.product_qty * rec.product_uom.factor_inv) / rec.product_uom_to.factor_inv
				elif rec.product_uom_to.uom_type == 'smaller':
					rec.product_qty_to = (rec.product_qty * rec.product_uom.factor) * rec.product_uom_to.factor
				elif rec.product_uom_to.uom_type == 'reference':
					rec.product_qty_to = rec.product_qty
			else:
				rec.product_qty_to = False



class StockMoveLine(models.Model):
	_inherit = "stock.move.line"

	product_uom_to = fields.Many2one('uom.uom', string='UoM To', domain="[('category_id', '=', product_uom_category_id)]")
	product_qty_to = fields.Float(string='Quantity To', compute = "_compute_product_qty_to")

	@api.onchange('product_uom_to', 'product_qty')
	def _compute_product_qty_to(self):
		for rec in self:
			if rec.product_uom_to:
				if rec.product_uom_to.uom_type == 'bigger':
					rec.product_qty_to = (rec.qty_done * rec.product_uom_id.factor_inv) / rec.product_uom_to.factor_inv
				elif rec.product_uom_to.uom_type == 'smaller':
					rec.product_qty_to = (rec.qty_done * rec.product_uom_id.factor) * rec.product_uom_to.factor
				elif rec.product_uom_to.uom_type == 'reference':
					rec.product_qty_to = rec.qty_done
			else:
				rec.product_qty_to = False


	def _get_aggregated_product_quantities(self, **kwargs):
		""" Returns a dictionary of products (key = id+name+description+uom) and corresponding values of interest.

		Allows aggregation of data across separate move lines for the same product. This is expected to be useful
		in things such as delivery reports. Dict key is made as a combination of values we expect to want to group
		the products by (i.e. so data is not lost). This function purposely ignores lots/SNs because these are
		expected to already be properly grouped by line.

		returns: dictionary {product_id+name+description+uom: {product, name, description, qty_done, product_uom}, ...}
		"""
		aggregated_move_lines = {}
		for move_line in self:
			name = move_line.product_id.display_name
			description = move_line.move_id.description_picking
			if description == name or description == move_line.product_id.name:
				description = False
			uom = move_line.product_uom_id
			line_key = str(move_line.product_id.id) + "_" + name + (description or "") + "uom " + str(uom.id)

			if line_key not in aggregated_move_lines:
				aggregated_move_lines[line_key] = {'name': name,
													'description': description,
													'qty_done': move_line.qty_done,
													'product_uom': uom.name,
													'product': move_line.product_id,
													'product_uom_to': move_line.product_uom_to,
													'product_qty_to': move_line.product_qty_to}
			else:
				aggregated_move_lines[line_key]['qty_done'] += move_line.qty_done
		return aggregated_move_lines