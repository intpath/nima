# -*- coding: utf-8 -*-

from odoo import models, fields, api

# CREATED AND EDITED BY SHAMS@INTEGRATED_PATH
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    lot_date = fields.Datetime(string="Lot Expire Date", readonly=True, related="lot_id.expiration_date", translate=True)
    lot_note = fields.Html(string="Lot Note", readonly=True, related="lot_id.note", translate=True)
    left_qty = fields.Float(string="Quantity Left", compute="calc_deliverd", translate=True)

    @api.constrains("lot_id")
    def compute_lot_date(self):
        for line in self:
            if line.lot_id:
                line.lot_date = line.lot_id.expiration_date
                line.lot_note = line.lot_id.note

    # @api.depends("order_line")
    def calc_deliverd(self):
        for order_line in self:
            if order_line.qty_delivered:
                order_line.left_qty=order_line.product_uom_qty-order_line.qty_delivered

            else:
                order_line.left_qty=0.0
