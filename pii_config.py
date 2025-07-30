# PII Protection Configuration
# Customize these settings based on your organization's requirements

# PII entities to detect and anonymize
PII_ENTITIES = [
    "PERSON",           # Personal names
    "EMAIL_ADDRESS",    # Email addresses  
    "PHONE_NUMBER",     # Phone numbers
    "CREDIT_CARD",      # Credit card numbers
    "US_SSN",          # Social Security Numbers
    "IP_ADDRESS",       # IP addresses
    "LOCATION",         # Addresses, locations
    "ORGANIZATION",     # Company names (optional - may remove context)
    "US_DRIVER_LICENSE" # Driver's license numbers
    # NOTE: DATE_TIME excluded - incident timestamps are operational data, not PII
]

# Optional entities (may affect context but provide privacy)
OPTIONAL_ENTITIES = [
    "DATE_TIME",        # Specific dates/times (may affect incident timeline)
    "ORGANIZATION",     # Company names (may affect categorization)
    "URL",             # URLs in incident notes
    "IBAN_CODE",       # International bank account numbers
    "NRP",             # Natural person references
]

# Anonymization strategies
ANONYMIZATION_STRATEGIES = {
    "PERSON": {
        "strategy": "replace",
        "replacement": "[PERSON]"
    },
    "EMAIL_ADDRESS": {
        "strategy": "replace", 
        "replacement": "[EMAIL]"
    },
    "PHONE_NUMBER": {
        "strategy": "replace",
        "replacement": "[PHONE]"
    },
    "CREDIT_CARD": {
        "strategy": "replace",
        "replacement": "[CREDIT_CARD]"
    },
    "US_SSN": {
        "strategy": "replace",
        "replacement": "[SSN]"
    },
    "IP_ADDRESS": {
        "strategy": "replace",
        "replacement": "[IP_ADDRESS]"
    },
    "LOCATION": {
        "strategy": "replace",
        "replacement": "[LOCATION]"
    },
    "ORGANIZATION": {
        "strategy": "replace",
        "replacement": "[ORGANIZATION]"
    },
    "US_DRIVER_LICENSE": {
        "strategy": "replace",
        "replacement": "[DRIVER_LICENSE]"
    },
    "DATE_TIME": {
        "strategy": "replace",
        "replacement": "[DATETIME]"
    }
}

# Alternative strategies (can be used instead of simple replacement)
ALTERNATIVE_STRATEGIES = {
    # Mask with partial information
    "PHONE_NUMBER": {
        "strategy": "mask",
        "masking_char": "*",
        "chars_to_mask": 6,
        "from_end": True
    },
    # Hash for consistent anonymization
    "EMAIL_ADDRESS": {
        "strategy": "hash",
        "hash_type": "sha256"
    },
    # Generate synthetic data
    "PERSON": {
        "strategy": "replace",
        "replacement": "{{FAKE_PERSON}}"  # Would need faker library
    }
}

# Configuration flags
CONFIG = {
    # Enable/disable PII protection
    "enabled": True,
    
    # Log PII findings for compliance auditing
    "log_pii_findings": True,
    
    # Minimum confidence threshold (0.0 to 1.0)
    "min_confidence": 0.6,
    
    # Entities to exclude from detection (even if in PII_ENTITIES)
    "excluded_entities": ["DATE_TIME"],  # Preserve incident timeline data
    
    # Include optional entities
    "include_optional_entities": False,
    
    # Preserve incident structure (don't anonymize incident numbers, categories, etc.)
    "preserve_incident_structure": True
}

# Incident-specific settings
INCIDENT_PRESERVATION = {
    # Fields that should NOT be anonymized to preserve incident context
    "preserve_fields": [
        "incident_number",
        "category", 
        "subcategory",
        "priority",
        "state",
        "assignment_group"
    ],
    
    # Patterns to preserve (regex patterns)
    "preserve_patterns": [
        r"INC\d+",          # Incident numbers
        r"CHG\d+",          # Change requests
        r"PRB\d+",          # Problem records
        r"TASK\d+",         # Task numbers
    ]
}
