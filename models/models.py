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


class LotExt(models.Model):
    _inherit = 'stock.production.lot'
    expiration_date = fields.Datetime(string="Expiration Date")




class SaleOrderLineInherit(models.Model):
    _inherit="sale.order.line"
    
    lot_date = fields.Datetime(string="Lot Expire Date",readonly=True,related="lot_id.expiration_date")
    lot_note = fields.Html(string="Lot Note",readonly=True, related="lot_id.note")

    @api.constrains("lot_id")
    def compute_lot_date(self):
        for line in self:
            if line.lot_id:
                line.lot_date = line.lot_id.expiration_date
                line.lot_note = line.lot_id.note