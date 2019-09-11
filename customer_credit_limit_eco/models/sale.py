# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from odoo import api, models, fields
from odoo.exceptions import ValidationError

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError


class sale_order(models.Model):
    _inherit= 'sale.order'
    
    exceeded_amount = fields.Float('Exceeded Amount')
    hold_credit_limit = fields.Boolean('Hold Credit limit')
    
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('credit_limit', 'Credit limit'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')

    
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(sale_order,self).onchange_partner_id()
        if self.partner_id:
            if self.partner_id.credit_limit_on_hold:
                msg = "Customer '" + self.partner_id.name + "' is on credit limit hold."
                return {'warning':
                            {'title': 'Credit Limit On Hold', 'message': msg
                             }
                        }

    @api.multi
    def _action_confirm_wo_delivery(self):
        """ Implementation of additionnal mecanism of Sales Order confirmation.
            This method should be extended when the confirmation should generated
            other documents. In this method, the SO are in 'sale' state (not yet 'done').
        """
        if self.env.context.get('send_email'):
            self.force_quotation_send()

        # create an analytic account if at least an expense product
        if any([expense_policy != 'no' for expense_policy in self.order_line.mapped('product_id.expense_policy')]):
            if not self.analytic_account_id:
                self._create_analytic_account()
        return True

		
    @api.multi
    def action_confirm_wo_delivery(self):




        if self.partner_id.check_credit:
            domain = [
                ('order_id.partner_id', '=', self.partner_id.id),
                ('order_id.state', 'in', ['sale', 'credit_limit'])]
            order_lines = self.env['sale.order.line'].search(domain)
            
            order = []
            to_invoice_amount = 0.0
            for line in order_lines:
                not_invoiced = line.product_uom_qty - line.qty_invoiced
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(
                    price, line.order_id.currency_id,
                    not_invoiced,
                    product=line.product_id, partner=line.order_id.partner_id)
                if line.order_id.id not in order:
                    if line.order_id.invoice_ids:
                        for inv in line.order_id.invoice_ids:
                            if inv.state == 'draft':
                                order.append(line.order_id.id)
                                break
                    else:
                        order.append(line.order_id.id)
                    
                to_invoice_amount += taxes['total_included']
            
            domain = [
                ('invoice_id.partner_id', '=', self.partner_id.id),
                ('invoice_id.state', '=', 'draft'),
                ('sale_line_ids', '!=', False)]
            draft_invoice_lines = self.env['account.invoice.line'].search(domain)
            for line in draft_invoice_lines:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price, line.invoice_id.currency_id,
                    line.quantity,
                    product=line.product_id, partner=line.invoice_id.partner_id)
                to_invoice_amount += taxes['total_included']

            # We sum from all the invoices lines that are in draft and not linked
            # to a sale order
            domain = [
                ('invoice_id.partner_id', '=', self.partner_id.id),
                ('invoice_id.state', '=', 'draft'),
                ('sale_line_ids', '=', False)]
            draft_invoice_lines = self.env['account.invoice.line'].search(domain)
            draft_invoice_lines_amount = 0.0
            invoice=[]
            for line in draft_invoice_lines:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price, line.invoice_id.currency_id,
                    line.quantity,
                    product=line.product_id, partner=line.invoice_id.partner_id)
                draft_invoice_lines_amount += taxes['total_included']
                if line.invoice_id.id not in invoice:
                    invoice.append(line.invoice_id.id)

            available_credit = self.partner_id.credit_limit - self.partner_id.credit - to_invoice_amount - draft_invoice_lines_amount

            if self.amount_total > available_credit:
                # imd = self.env['ir.model.data']
                if self.hold_credit_limit == False:
                    raise ValidationError(_('Please be informed that the selected customer credit limit '+str(available_credit)+' is lower than the order amount '+str(self.amount_total)+''))
                # raise UserError("Please be informed that the selected customer credit limit'+available_credit+' is lower than the order amoun'+self.amount_total+'")
                # exceeded_amount = (to_invoice_amount + draft_invoice_lines_amount + self.partner_id.credit + self.amount_total) - self.partner_id.credit_limit
                # vals_wiz={
                #     'partner_id':self.partner_id.id,
                #     'sale_orders':str(len(order))+ ' Sale Order Worth : '+ str(to_invoice_amount),
                #     'invoices':str(len(invoice))+' Draft Invoice worth : '+ str(draft_invoice_lines_amount),
                #     'current_sale':self.amount_total or 0.0,
                #     'exceeded_amount':exceeded_amount,
                #     'credit':self.partner_id.credit,
                #     'credit_limit_on_hold':self.partner_id.credit_limit_on_hold,
                #     }
                # wiz_id = self.env['customer.limit.wizard'].create(vals_wiz)
                # action = imd.xmlid_to_object('dev_customer_credit_limit.action_customer_limit_wizard')
                # form_view_id = imd.xmlid_to_res_id('dev_customer_credit_limit.view_customer_limit_wizard_form')
                # return {
                        # 'name': action.name,
                        # 'help': action.help,
                        # 'type': action.type,
                        # 'views': [(form_view_id, 'form')],
                        # 'view_id': form_view_id,
                        # 'target': action.target,
                        # 'context': action.context,
                        # 'res_model': action.res_model,
                        # 'res_id':wiz_id.id,
                    # }

                if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                    raise UserError(_(
                        'It is not allowed to confirm an order in the following states: %s'
                        ) % (', '.join(self._get_forbidden_state_confirm())))

                for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                    order.message_subscribe([order.partner_id.id])
                self.write({
                    'state': 'sale',
                    'confirmation_date': fields.Datetime.now()
                })
                self._action_confirm_wo_delivery()
                if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                    self.action_done()
                return True
            else:

                if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                    raise UserError(_(
                        'It is not allowed to confirm an order in the following states: %s'
                        ) % (', '.join(self._get_forbidden_state_confirm())))

                for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                    order.message_subscribe([order.partner_id.id])
                self.write({
                    'state': 'sale',
                    'confirmation_date': fields.Datetime.now()
                })
                self._action_confirm_wo_delivery()
                if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                    self.action_done()
                return True
        else:
            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                    ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write({
                'state': 'sale',
                'confirmation_date': fields.Datetime.now()
            })
            self._action_confirm_wo_delivery()
            if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                self.action_done()
            return True
            
        
    @api.multi
    def _make_url(self,model='sale.order'):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
        if base_url:
            base_url += '/web/login?db=%s&login=%s&key=%s#id=%s&model=%s' % (self._cr.dbname, '', '', self.id, model)
        return base_url

    @api.multi
    def send_mail_approve_credit_limit(self): 
        manager_group_id = self.env['ir.model.data'].get_object_reference('sales_team', 'group_sale_manager')[1]
        browse_group = self.env['res.groups'].browse(manager_group_id) 
        
        url = self._make_url('sale.order')
        subject = self.name + '-' + 'Require to Credit Limit Approval'
        for user in browse_group.users:
            partner = user.partner_id
            body = '''
                        <b>Dear ''' " %s</b>," % (partner.name) + '''
                        <p> A Sale Order ''' "<b><i>%s</i></b>" % self.name + '''  for customer ''' "<b><i>%s</i></b>" % self.partner_id.name +''' require your Credit Limit Approval.</p> 
                        <p>You can access sale order from  below url <br/>
                        ''' "%s" % url +''' </p> 
                        
                        <p><b>Regards,</b> <br/>
                        ''' "<b><i>%s</i></b>" % self.user_id.name +''' </p> 
                        ''' 
            
            mail_values = {
                        'email_from': self.user_id.email,
                        'email_to': partner.email,
                        'subject': subject,
                        'body_html': body,
                        'state': 'outgoing',
                        'type': 'email',
                    }
            mail_id =self.env['mail.mail'].create(mail_values)
            mail_id.send(True)
