from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    leave_reviewer_id = fields.Many2one(
        'res.users',
        string="Leave Reviewer",
        help="Person responsible for reviewing leave requests",
        related="employee_id.leave_reviewer_id",
        store=True,
        readonly=False,
        tracking=True
    )

    def action_validate1(self):
        if not (self.leave_reviewer_id.id == self.env.uid and 
                self.env.user.has_group('dh_leave_mgt.group_hr_holidays_reviewer')):
            raise UserError(_("You are not authorized to review this leave request."))
        if self.employee_id.user_id.partner_id:
            self.message_post(
                body=_("Leave request is under review."),
                partner_ids=[self.employee_id.user_id.partner_id.id]
            )
        return super(HrLeave, self).action_validate1()

    def action_validate(self):
        if self.state != 'validate1':
            raise UserError(_("Only reviewed leaves can be approved."))
        return super(HrLeave, self).action_validate()

    def action_refuse(self):
        self.ensure_one()
        return super(HrLeave, self).action_refuse()

    def action_draft(self):
        self.ensure_one()
        return super(HrLeave, self).action_draft()
