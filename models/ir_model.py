from odoo import models, api

class IrModel(models.Model):
    _inherit = 'ir.model'
    
    @api.model
    def create_and_get_rules(self, model_name, rules_data):
        """Create IR rules for a model
        
        Args:
            model_name: String name of the model
            rules_data: List of dictionaries with rule data
            
        Returns:
            List of created rule IDs
        """
        model = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
        if not model:
            return False
            
        rule_ids = []
        for rule_data in rules_data:
            # Add model_id to the rule data
            rule_data['model_id'] = model.id
            # Create the rule
            rule = self.env['ir.rule'].create(rule_data)
            rule_ids.append(rule.id)
            
        return rule_ids
