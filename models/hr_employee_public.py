from odoo import fields, models

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    leave_reviewer_id = fields.Many2one('res.users', readonly=True)
