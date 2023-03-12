# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    activity_mode = fields.Selection(
        string="Activity Mode",
        selection=[
            ('list_executable', "List: Executable"),
            ('list_incubator', "List: Incubator"),
            ('tickler_file_short_term', "Tickler File: Short Term"),
            ('tickler_file_long_term', "Tickler File: Long Term"),
            ('tickler_file_recurring_tasks', "Tickler File: Recurring Tasks"),
    ]
    )
