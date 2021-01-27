# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class nima(models.Model):
#     _name = 'nima.nima'
#     _description = 'nima.nima'

class SaleOrderExt(models.Model):
    _inherit = 'sale.order'


class InvoiceReportExt(models.Model):
    _inherit = 'account.move'
    req_qty = fields.Float(string = "Required Quantity")
    left_qty  = fields.Float(compute='count_left_item')


    @api.depends("invoice_line_ids")
    def count_left_item(self):
        for line in self.invoice_line_ids:
            if self.req_qty:
                self.left_qty=self.req_qty-line.quantity
            else: 
                self.left_qty=0.0



