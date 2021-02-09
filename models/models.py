# -*- coding: utf-8 -*-

from odoo import models, fields, api

# CREATED AND EDITED BY SHAMS@INTEGRATED_PATH
class SaleOrderLineInherit(models.Model):
    _inherit="sale.order.line"
    
    lot_date = fields.Datetime(string="Lot Expire Date",readonly=True,related="lot_id.expiration_date")
    lot_note = fields.Html(string="Lot Note",readonly=True, related="lot_id.note")
    left_qty=fields.Float(string="Quantity Left",compute="calc_deliverd")


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
    qty_delivered=fields.Float(string='Quantity Delivered',compute="calc_deliverd")
    left_qty=fields.Float(string="Quantity Left",compute="calc_deliverd")


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



# class SaleOrderExt(models.Model):
#     _inherit="sale.order"
#     user_id=fields.Many2one('res.users',compute="get_user_id") 

    # @api.depends('res.users')
    # def get_user_id(self):
    #     for sale_order in self:
    #         self.user_id=sale_order.user_id

            # user=self.env["stock.picking"].search([("origin","=",sale_order.name)])




# in case i didnt delivered anything : qty_delievered is zero 
# in case i delivered all the quantity : qty_delivered is quantity 