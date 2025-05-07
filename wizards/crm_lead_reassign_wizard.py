from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmLeadReassignWizard(models.TransientModel):
    _name = 'crm.lead.reassign.wizard'
    _description = 'Lead Reassignment Wizard'

    reassign_type = fields.Selection([
        ('team_only', 'Reassign Team Only'),
        ('salesperson_only', 'Reassign Salesperson Only'),
        ('both', 'Reassign Both Team and Salesperson')
    ], string='Reassignment Type', default='both', required=True)
    
    result = fields.Text(string='Result', readonly=True)
    
    def action_reassign(self):
        """Reassign selected leads to proper teams/salespeople based on preferred branch"""
        # Get selected lead ids from context
        lead_ids = self.env.context.get('active_ids', [])
        leads = self.env['crm.lead'].browse(lead_ids)
        
        if not leads:
            raise UserError(_("No leads selected for reassignment."))
        
        # Initialize counters for the report
        reassigned_team_count = 0
        reassigned_user_count = 0
        not_reassigned_count = 0
        
        for lead in leads:
            branch = lead.preferred_branch or lead.city  # Try preferred_branch first, then city
            if not branch:
                not_reassigned_count += 1
                continue
                
            # Normalize branch name
            normalized_branch = branch.strip().lower().rstrip('_')
            
            # Find matching team
            team = False
            reassigned_team = False
            teams = self.env['crm.team'].search([('preferred_branches', '!=', False)])
            
            for t in teams:
                team_branches = t._get_normalized_branches()
                if normalized_branch in team_branches:
                    team = t
                    break
            
            # Reassign team if found and requested
            if team and self.reassign_type in ['team_only', 'both']:
                if lead.team_id != team:
                    lead.team_id = team.id
                    reassigned_team_count += 1
                    reassigned_team = True
            
            # Reassign salesperson if requested
            if self.reassign_type in ['salesperson_only', 'both']:
                if team and reassigned_team:
                    # Get a random member from the team
                    members = team.member_ids
                    if members:
                        random_member = members[0]  # For simplicity, get the first member
                        if lead.user_id != random_member:
                            lead.user_id = random_member.id
                            reassigned_user_count += 1
                    
            # If no reassignment happened
            if not (reassigned_team or (self.reassign_type in ['salesperson_only', 'both'] and reassigned_user_count > 0)):
                not_reassigned_count += 1
        
        # Set the result message
        result_message = _("""
Reassignment completed:
- Leads with team reassigned: %(team_count)s
- Leads with salesperson reassigned: %(user_count)s
- Leads not reassigned (no match found): %(not_reassigned)s
        """) % {
            'team_count': reassigned_team_count,
            'user_count': reassigned_user_count,
            'not_reassigned': not_reassigned_count,
        }
        
        self.write({'result': result_message})
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead.reassign.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
