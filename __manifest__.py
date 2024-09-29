# -*- coding: utf-8 -*-
{
    'name': "zk_controller",

    'summary': "ZK Integration Attandences Devices",

    'description': """
                        Long description of module's purpose
                    """,

    'author': "Ali M. Alhashim",
    'website': "https://www.ali-alhashim.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

