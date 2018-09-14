# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv, orm
from openerp.tools import html2plaintext
import re

class CrmHelpdesk(osv.osv):

    _inherit = "crm.helpdesk"

    def _prepare_message_new_custom_values(self, cr, uid, msg,
                                           custom_values=None, context=None):
        custom_values, msg = super(
            CrmHelpdesk, self)._prepare_message_new_custom_values(
            cr, uid, msg, custom_values=custom_values, context=context
        )

        def parse_description(description):
            fields = ['email', 'first & last name']
            _dict = {}
            description = description.lower()
            for line in description.split('\n'):
                for field in fields:
                    if field in line:
                        split_line = line.split(':')
                        if len(split_line) > 1:
                            _dict[field] = line.split(':')[1].strip()
            return _dict
        subject = msg.get('subject', '')
        subject = subject.lower()
        if 'support inquiry' in subject:
            if custom_values is None:
                custom_values = {}
            desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
            _dict = parse_description(desc)
            contact_name = False
            email_from = False
            if _dict.get('email'):
                email_from = re.sub("\s\[\d\]", "", _dict.get('email')).strip()
            if _dict.get('first & last name'):
                contact_name = _dict.get('first & last name').title()
            # Search for an existing partner:
            # Search for an existing partner:
            if contact_name and email_from:
                partner_id = self.pool.get('res.partner').search(cr, uid, [
                    '|', ('name', '=', contact_name),
                    ('email', '=', email_from)], context=context, limit=1)
            elif contact_name and not email_from:
                partner_id = self.pool.get('res.partner').search(cr, uid, [
                    ('name', '=', contact_name)], context=context, limit=1)
            elif email_from and not contact_name:
                partner_id = self.pool.get('res.partner').search(cr, uid, [
                    ('email', '=', email_from)], context=context, limit=1)
            else:
                partner_id = False
            vals = {
                'email_from': email_from,
                'contact_name': contact_name,
                'partner_id': partner_id[0] if partner_id else False,
            }
            msg['from'] = _dict.get('email')
            custom_values.update(vals)
        return custom_values, msg
