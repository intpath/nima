# -*- coding: utf-8 -*-
{
    'name': "Nima",

    'summary': """Edits on Invoice and Sale Order and Delivery Slip Reports""",

    'author': "INTEGRATED PATH",
    'website': "https://www.int-path.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'sale', 'stock', 'account', 'product', 
        'mrp', 'mai_sale_order_lot_selection', 'product_expiry'
    ],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/sale_order.xml',
        'views/invoice_report.xml',
        'views/stock_picking_views.xml',
        'report/deleivery_slip_ext.xml',
    ],
}
