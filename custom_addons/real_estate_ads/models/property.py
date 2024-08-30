from odoo import fields, models, api, _

# 87a8a8b900e0d6bbdd486959a6599d88+speech_mu+gu_in_23_publicaudio_review+INTERNAL+en:4029242593440410961
class Property(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.published.mixin', 'website.seo.metadata'] # mail.alias.mixin, utm.mixin,
    _description = "Estate Properties"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
         ("new", "New"),
         ("received", "Offer Received"),
         ("accepted", "Offer Accepted"),
         ("sold", "Sold"),
         ("cancel", "Cancelled")
    ], string="Status", default="new")
    tags_id = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Monetary(string="Expected Price", tracking=True)
    best_offer = fields.Monetary(string="Best Offer", compute="compute_best_price")
    selling_price = fields.Monetary(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        string="Garden Orientation", default="north")
    offer_id = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[(['is_company', '=', True])])
    phone = fields.Char(string='Phone', related="buyer_id.phone")
    total_area = fields.Integer(string="Total Area", compute="compute_total_area")
    offer_count = fields.Integer(string="Offer Count", compute="compute_offer_count")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('garden_area', 'living_area')
    def compute_total_area(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area
            print(rec.garden_area)
            print(rec.living_area)

    def action_sold(self):
        self.state = "sold"

    def action_cancel(self):
        self.state = "cancel"

    @api.depends('offer_id')
    def compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_id)

    # python version for a button using object instead of object

    # def action_property_view_offer(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': f"{self.name} - Offers",
    #         'domain': [('property_id', '=', self.id)],
    #         'view_mode': 'tree',
    #         'res_model': 'estate.property.offer',
    #     }

    @api.depends('offer_id')
    def compute_best_price(self):
        for rec in self:
            if rec.offer_id:
                rec.best_offer = max(rec.offer_id.mapped('price'))
                print("best offer : ", rec.best_offer)
            else:
                rec.best_offer = 0

   # Just to understand client actions using inbuilt or existing odoo tags

    # def action_client_action(self):
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification', # apps, reload,
    #         'params': {
    #             'title': _('Testing Client'),
    #             'type': 'success' # danger, success, warning,
    #             'sticky': False
    #         }
    #     }


    # URL Action Demonstration

    # def action_url_action(self):
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': "https:/odoo.com",
    #         'target': 'self', # new, tree, self
    #     }

    # Understanding - Report actions

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate Property - %s' % self.name

    # Website Published Mixin Demo

    def _compute_website_url(self):
        for rec in self:
            rec.website_url = '/properties/%s' % rec.id



    def action_email(self):
        mail_template = self.env.ref('real_estate_ads.offer_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self):
        return ','.join(self.offer_id.mapped('partner_email'))

    # @api.onchange('garden_area', 'living_area')
    # def onchange_total_area(self):
    #     self.total_area = self.garden_area + self.living_area
    #
    # total_area = fields.Integer(string="Total Area")

    # @api.auto_vacuum
    # def clean_offers(self):
    #     self.search([('status', '=', 'refused')]).unlink()


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(string="Name", required=True)

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
