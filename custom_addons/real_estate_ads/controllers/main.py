from odoo import http
from odoo.http import request

# To inherit Controllers of one module to another

# from odoo.addons.real_estate_ads.controllers.main import PropertyController

# class PropertyController(PropertyController):


class PropertyController(http.Controller):

    @http.route(["/properties"], type='http', website=True, auth='public') # , methods="POST", cors="*", csrf=True
    def show_properties(self):
        property_ids = request.env['estate.property'].search([])
        print(property_ids)
        return request.render("real_estate_ads.property_list", {"property_ids": property_ids})