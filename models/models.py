# -*- coding: utf-8 -*-

from odoo import models, fields, api

# CREATED AND EDITED BY SHAMS@INTEGRATED_PATH
class SaleOrderLineInherit(models.Model):
    _inherit="sale.order.line"
    
    lot_date = fields.Datetime(string="Lot Expire Date",readonly=True,related="lot_id.expiration_date", translate=True)
    lot_note = fields.Html(string="Lot Note",readonly=True, related="lot_id.note", translate=True)
    left_qty=fields.Float(string="Quantity Left",compute="calc_deliverd", translate=True)


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
                 
      


class InvoiceLineExt(models.Model):
    _inherit="account.move.line"
    qty_delivered=fields.Float(string='Quantity Delivered',compute="calc_deliverd", translate=True)
    left_qty=fields.Float(string="Quantity Left",compute="calc_deliverd",translate=True)


    @api.depends("sale_line_ids")
    def calc_deliverd(self):
        for invoice_line in self:
            sale_order_line=invoice_line.sale_line_ids
            if sale_order_line:
                invoice_line.qty_delivered=sale_order_line.qty_delivered
                invoice_line.left_qty=sale_order_line.product_uom_qty-sale_order_line.qty_delivered

            else:
                invoice_line.qty_delivered=0.0
                invoice_line.left_qty=0.0




class StockPickingExt(models.Model):
    _inherit="stock.picking"
    driver_name = fields.Char(string = "Driver name", translate=True)
    veh_num = fields.Char(string = "Vehical number", translate=True)