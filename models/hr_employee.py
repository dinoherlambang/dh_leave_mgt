from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_manager_id = fields.Many2one(
        'res.users',
        string='Approver',  # Changed from 'Time Off' to 'Approver'
    )
    
    leave_reviewer_id = fields.Many2one(
        'res.users',
        string='Leave Reviewer',
        tracking=True,
        help="Person responsible for reviewing leave requests"
    )
