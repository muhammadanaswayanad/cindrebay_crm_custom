{
    'name': 'Cindrebay CRM Custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom fields for CRM Lead',
    'depends': [
        'base',
        'crm',
        'sale',
        'sale_crm',
        'hr',  # for employee reference
        'mail',  # for activity type
    ],
    'data': [
        'security/record_rules.xml',  # Changed back to original filename
        'security/ir.model.access.csv',
        'data/activity_data.xml',
        'data/sequence.xml',  # New sequence data
        'views/crm_lead_views.xml',
        'views/res_partner.xml',
        'views/crm_views.xml',
        'views/crm_walkin_views.xml',  # New walkin views
        'views/crm_team_views.xml',
        'views/crm_lead_reassign_views.xml',
    ],
    'installable': True,
    'application': False,
}
