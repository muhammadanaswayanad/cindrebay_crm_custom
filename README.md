# Cindrebay CRM Custom

## Features

### Lead Assignment Logic

The module provides two methods for assigning leads to sales teams:

1. **Branch-Based Assignment**: Leads are assigned to teams based on matching the lead's `preferred_branch` field with the team's `preferred_branches` field.

2. **Random Assignment**: If no branch match is found, leads are assigned randomly to sales teams as a fallback.

## Configuration

### Sales Teams

- Go to CRM > Configuration > Sales Teams
- For each team, set the `Preferred Branches` field to a comma-separated list of branches this team handles
- Example: "kochi, calicut, trivandrum"

### Lead Assignment

When a lead is created or its preferred branch is updated:
1. The system attempts to find a matching sales team based on the preferred branch
2. If found, the lead is assigned to that team
3. If no match is found, the lead is assigned randomly to a sales team

## Technical Notes

- Branch matching is case-insensitive and ignores trailing underscores and whitespace
- Example: "kochi_", "Kochi", and "kochi" are all considered the same branch