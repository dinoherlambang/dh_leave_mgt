from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('in_review', 'In Review'),
        ('validate', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True, copy=False)

    leave_reviewer_id = fields.Many2one(
        'res.users',
        string="Leave Reviewer",
        help="Person responsible for reviewing leave requests",
        related="employee_id.leave_reviewer_id",
        store=True,
        readonly=False,
        tracking=True
    )

    can_review = fields.Boolean(
        string='Can Review',
        compute='_compute_can_review',
        help="Technical field used to determine if user can review the leave"
    )

    @api.depends('leave_reviewer_id', 'state')
    def _compute_can_review(self):
        for leave in self:
            leave.can_review = (
                leave.state in ['draft', 'confirm'] and 
                leave.leave_reviewer_id and 
                leave.leave_reviewer_id.id == self.env.uid and
                self.env.user.has_group('dh_leave_mgt.group_hr_holidays_reviewer')
            )

    def action_review(self):
        self.ensure_one()
        if not self.can_review:
            raise UserError(_("You are not authorized to review this leave request."))
        self.write({'state': 'in_review'})
        if self.employee_id.user_id.partner_id:
            self.message_post(
                body=_("Leave request is under review."),
                partner_ids=[self.employee_id.user_id.partner_id.id]
            )
        return True

    def action_validate(self):
        self.ensure_one()
        if self.state != 'in_review':
            raise UserError(_("Only reviewed leaves can be approved."))
        self.write({'state': 'validate'})
        return True

    def action_refuse(self):
        self.ensure_one()
        self.write({'state': 'refuse'})
        return True

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancel'})
        return True
