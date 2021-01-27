# -*- coding: utf-8 -*-
# from odoo import http


# class Nima(http.Controller):
#     @http.route('/nima/nima/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nima/nima/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nima.listing', {
#             'root': '/nima/nima',
#             'objects': http.request.env['nima.nima'].search([]),
#         })

#     @http.route('/nima/nima/objects/<model("nima.nima"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nima.object', {
#             'object': obj
#         })
