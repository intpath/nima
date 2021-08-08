# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
	_inherit = "stock.move"

	@api.model
	def create(self, values):
		if values.get('purchase_line_id'):
			purchase_line_id  = self.env['purchase.order.line'].browse( values['purchase_line_id'] )
			values['product_uom'] = purchase_line_id.product_uom.id
			values['product_uom_qty'] = purchase_line_id.product_qty
		
		res = super(StockMove, self).create(values)
		return res