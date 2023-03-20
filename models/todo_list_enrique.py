# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from collections import Counter


class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = ['mail.activity', 'mail.thread']
    _rec_name = 'summary'

    date_deadline = fields.Date('Due Date', index=True, required=True,
                                default=fields.Date.context_today, store=True)
    user_id = fields.Many2one('res.users', string='user', index=True,
                              tracking=True, default=lambda self: self.env.user)
    res_model_id = fields.Many2one(
        'ir.model', 'Document Model',
        index=True, ondelete='cascade', required=True,
        default=lambda self: self.env.ref('todo_list_EnriqueCT.model_activity_general'))
    res_id = fields.Many2oneReference(string='Related Document ID', index=True,
                                      required=True, model_field='res_model',
                                      default=lambda self: self.env.ref(
                                          'todo_list_EnriqueCT.general_activities'))
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Importante'),
        ('2', 'Muy Importante'),
        ('3', 'Urgente'),
    ], default='0', index=True, store=True)
    activity_gtd = fields.Selection(
        string="Activity GTD",
        selection=[
            ('list_executable', "Lista: Ejecutable"),
            ('tickler_file_recurring_tasks', "Tickler File: Tareas Recurrentes"),
            ('tickler_file_short_term', "Tickler File: Corto Plazo"),
            ('tickler_file_long_term', "Tickler File: Largo Plazo"),
            ('list_incubator', "Lista: Incubadora"),
            ('archived', "Archived"),])
    days_remaining = fields.Integer(
        string='Días restantes',
        compute='_compute_remaining_days',
        store=False,
        compute_sudo=True,
    )
    state = fields.Selection([
        ('today', 'Hoy'),
        ('planned', 'Planificado'),
        ('done', 'Hecho'),
        ('overdue', 'Caducado'),
        ('cancel', 'Cancelado'), ], 'State',
        compute='_compute_state', store=True)
    interval = fields.Selection(
        [('Daily', 'Diario'),
         ('Weekly', 'Semanal'),
         ('Monthly', 'Mensual'),
         ('Quarterly', 'Trimestral'),
         ('Yearly', 'Anual')],
        string='Intervalo Recurrente', )
    new_date = fields.Date(string="Siguiente fecha de vencimiento", store=True)

    def action_done(self):
        """Función del botón Hecho"""
        self.write({'state': 'done'})
        if self.activity_gtd == 'tickler_file_recurring_tasks':
            self.env['mail.activity'].create({
                'res_id': self.res_id,
                'res_model_id': self.res_model_id.id,
                'summary': self.summary,
                'priority': self.priority,
                'date_deadline': self.new_date,
                'activity_gtd': self.activity_gtd,
                'interval': self.interval,
                'activity_type_id': self.activity_type_id.id,
                'new_date': self.get_date(),
                'user_id': self.user_id.id
            })
        self.write({'activity_gtd': 'archived'})

    def get_date(self):
        """ Función para obtener la nueva fecha de vencimiento en un nuevo registro"""
        date_deadline = self.new_date if self.new_date else self.date_deadline
        new_date = False
        if self.interval == 'Daily':
            new_date = (
                    date_deadline + timedelta(days=1)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        elif self.interval == 'Weekly':
            new_date = (
                    date_deadline + timedelta(days=7)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        elif self.interval == 'Monthly':
            new_date = (
                    date_deadline + timedelta(days=30)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        elif self.interval == 'Quarterly':
            new_date = (
                    date_deadline + timedelta(days=90)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        elif self.interval == 'Yearly':
            new_date = (
                    date_deadline + timedelta(days=365)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        elif self.activity_gtd == 'tickler_file_short_term':
            new_date = (
                    date_deadline + timedelta(days=1)).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
        return new_date

    @api.onchange('interval', 'date_deadline')
    def onchange_recurring(self):
        """ Función para mostrar la nueva fecha de vencimiento"""
        self.new_date = False
        if self.activity_gtd == 'tickler_file_recurring_tasks' or 'tickler_file_short_term':
            self.new_date = self.get_date()

    def action_date(self):
        """ Función para acciones automáticas en la fecha de vencimiento"""
        today = fields.date.today()
        dates = self.env['mail.activity'].search(
            [('state', 'in', ['today', 'planned']),
             ('activity_gtd', 'in', ['tickler_file_recurring_tasks','tickler_file_short_term']),
             ('date_deadline', '=', today)])
        for rec in dates:
            self.env['mail.activity'].create(
                {'res_id': rec.res_id,
                 'res_model_id': rec.res_model_id.id,
                 'summary': rec.summary,
                 'priority': rec.priority,
                 'interval': rec.interval,
                 'date_deadline': rec.new_date,
                 'new_date': rec.get_date(),
                 'activity_type_id': rec.activity_type_id.id,
                 'user_id': rec.user_id.id
                 })
            rec.state = 'done'
            rec.activity_gtd = 'archived'

    def action_cancel(self):
        """ Función para el botón Cancelar"""
        return self.write({'state': 'cancel'}, {'activity_gtd': 'archived'})
    
    @api.depends('date_deadline')
    def _compute_remaining_days(self):
        today = fields.Date.today()
        for request in self.filtered('date_deadline'):
            if request.date_deadline:
                delta = today - request.date_deadline
                if delta.days < 0:
                    request.days_remaining = abs(delta.days)
                else:
                    request.days_remaining = 0
            else:
                request.days_remaining = 0


class ActivityGeneral(models.Model):
    _name = 'activity.general'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')

class ResUsers(models.Model):
    _inherit = 'res.users'

    scheduled_activities_ids = fields.One2many('mail.activity', 'user_id', string='Tareas programadas')
    assigned_activities_ids = fields.Many2many(
        'mail.activity',
        string='Tareas Asignadas',
    )
