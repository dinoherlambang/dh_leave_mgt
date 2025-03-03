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

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('validate1', 'In-Review'),
        ('refuse', 'Refused'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, tracking=True, copy=False, default='draft',
    help="The status is set to 'To Submit', when a time off request is created." +
    "\nThe status is 'To Approve', when time off request is confirmed by user." +
    "\nThe status is 'Refused', when time off request is refused by manager." +
    "\nThe status is 'Approved', when time off request is approved by manager.")

    # @api.model
    # def _selection_state(self):
    #     states = [
    #         ('draft', 'To Submit'),
    #         ('cancel', 'Cancelled'),
    #         ('confirm', 'To Approve'),
    #         ('validate1', 'In-Review'),
    #         ('refuse', 'Refused'),
    #         ('validate', 'Approved')
    #     ]
    #     return states

    # method which overrides the state label display while maintaining the underlying 'validate1' state value.
    # @api.model
    # def _get_state_from_name(self):
    #     states = super(HrLeave, self)._get_state_from_name()
    #     states['validate1'] = _('In-Review')
    #     return states
    
    # def _get_selection_state(self):
    #     states = super(HrLeave, self)._get_selection_state()
    #     states[1] = ('validate1', _('In-Review'))
    #     return states

    def action_approve(self):
        if not (self.leave_reviewer_id.id == self.env.uid and 
                self.env.user.has_group('dh_leave_mgt.group_hr_holidays_reviewer')):
            raise UserError(_("You are not authorized to review this leave request."))
        if self.employee_id.user_id.partner_id:
            self.message_post(
                body=_("Leave request is under review."),
                partner_ids=[self.employee_id.user_id.partner_id.id]
            )
        self.write({'state': 'validate1'})
        return True

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
