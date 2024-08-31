from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


# class PropertyOffer(models.AbstractModel):
#     _name = "abstract.property.offer"
#     _description = "Abstract Offers"
#
#     partner_email = fields.Char(string="E-mail")
#     partner_phone = fields.Float(string="Phone")


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    # _inherit = ['abstract.property.offer']
    _description = "Estate Property Offers"

    @api.depends('partner_id', 'property_id')
    def compute_name(self):
        for rec in self:
            if rec.partner_id and rec.property_id:
                rec.name = f"{rec.partner_id.name} - {rec.property_id.name}"
                # print(rec.partner_id.name)
                # print(rec.property_id.name)
            else:
                rec.name = False

    name = fields.Char(string="Description", compute="compute_name")
    price = fields.Monetary(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    partner_email = fields.Char(string="Customer Email", related="partner_id.email")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute="compute_deadline", inverse="inverse_deadline")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.model
    def set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=set_create_date)

    @api.depends('validity', 'creation_date')
    # @api.depends_context('uid')
    def compute_deadline(self):
        for rec in self:
            # print(self.env.context)
            # print(self._context)
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def inverse_deadline(self):
        for rec in self:
            if rec.creation_date and rec.deadline:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    # Used to create multiple records from single or multiple dictionary

    # @api.model_create_multi
    # def create(self, vals):
    #     for rec in vals:
    #         if not rec.get('creation_date'):
    #             rec['creation_date'] = fields.Date.today()
    #     return super(PropertyOffer, self).create(vals)


    # to prevent certain action or execution prior happening
    @api.constrains('validity')
    def check_validity(self):
        if self.validity:
            for rec in self:
                if rec.deadline <= rec.creation_date:
                    raise ValidationError("Deadline cannot be before creation date")

    def action_accept_offer(self):
        if self.property_id:
            self.validate_accept_offer()
            self.property_id.write({
                "selling_price": self.price,
                "state": "accepted"
            })
            # self.property_id.selling_price = self.price
        self.status = 'accepted'

    def validate_accept_offer(self):
        offer_id = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])
        if offer_id:
            raise ValidationError("You have accepted an offer already")

    def action_decline_offer(self):
        self.status = 'refused'
        print(all(self.property_id.offer_id.mapped('status')))
        print(self.property_id.offer_id.mapped('status'))
        if all(self.property_id.offer_id.mapped('status')):
            self.property_id.write({
                "selling_price": 0,
                "state": "received"
            })

    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids', [])
        # print(active_ids)
        if active_ids:
            offer_ids = self.env['estate.property.offer'].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1

    # SQL version of constraint to work with

    # _sql_constraints = [
    #     ('check_validity', 'check(validity>0)', 'Deadline cannot be before creation date')
    # ]

    # def write(self, vals):
    #     print(self)
    #     print(self.env.cr)
    #     print(self.env.uid)
    #     print(self.env.context)
    #     print(vals)
    #     res_partner_ids = self.env['res.partner'].search([
    #         ('is_company', '=', True)
    #         # ('name','=',vals.get('name')),
    #     ]).filtered(lambda c: c.phone == '(941)-284-4875') #.mapped('phone') #.unlink()  # , limit=2, order='name desc'
    #     print(res_partner_ids)

        # for rec in vals:
        # res_partner_ids = self.env['res.partner'].browse(10)
        # print(res_partner_ids)
        # print(res_partner_ids.name)
        # return super(PropertyOffer, self).write(vals)
