from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    state = fields.Selection(selection_add=[('in_review', 'In-Review')])

    leave_reviewer_id = fields.Many2one(
        'res.users',
        string="Leave Reviewer",
        help="Person responsible for reviewing leave requests",
        related="employee_id.leave_reviewer_id",
        store=True,
        readonly=False
    )

    can_review = fields.Boolean(
        string='Can Review',
        compute='_compute_can_review',
        store=False,
    )

    @api.depends('leave_reviewer_id', 'state')
    def _compute_can_review(self):
        """Compute if current user can review the leave request"""
        for leave in self:
            leave.can_review = (
                leave.state == 'draft' and 
                leave.leave_reviewer_id and 
                leave.leave_reviewer_id.id == self.env.uid and
                self.env.user.has_group('dh_leave_mgt.group_hr_holidays_reviewer')
            )

    def action_review(self):
        self.ensure_one()
        if not self.can_review:
            raise UserError(_("You are not authorized to review this leave request."))
        if self.state != 'draft':
            raise UserError(_("Only draft leaves can be reviewed."))
        self.write({'state': 'in_review'})
        return True

    def action_confirm(self):
        for leave in self:
            if leave.state != 'in_review':
                raise UserError(_("Leave must be reviewed before submitting."))
        return super(HrLeave, self).action_confirm()
