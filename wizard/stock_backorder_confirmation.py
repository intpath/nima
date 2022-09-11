# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockBackorderConfirmation(models.TransientModel):
	_inherit = "stock.backorder.confirmation"

	def process(self):
		res = super(StockBackorderConfirmation, self.with_context(nima_is_backorder=True)).process()
		return res