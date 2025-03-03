{
    'name': 'Leave Management',
    'version': '13.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Add reviewer in employee leave management',
    'description': """
        This module adds a reviewer field to employee leave management.
    """,
    'depends': ['hr', 'hr_holidays'],
    'data': [
        'security/hr_leave_security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_leave_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
