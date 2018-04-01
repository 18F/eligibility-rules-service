import json

schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "title": "Application",
    "description": "A set of applications, one per household",
    "definitions": {
        "ynexception": {
            "oneOf": [{
                "type": "boolean",
            }, {
                "type": "string",
                "value": "Exception",
            }],
        },
    },
    "type": "array",
    "items": {
        "title": "applications",
        "type": "object",
        "properties": {
            "all_applicants_present": {
                "$ref": "#/definitions/ynexception",
                "description":
                "All household's applicants are physically present",
            },
            "number_in_economic_unit": {
                "type": "integer",
                "default": 1,
            },
            "referrer_state": {
                "type": "string"
            },
            "applicants": {
                "description":
                "Individuals (adults or children) to receive benefits",
                "type":
                "array",
                "items": {
                    "title": "applicant",
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description":
                            "Unique identifier within a submission",
                        },
                        "birthdate": {
                            "type": ["string", "null"],
                            "description":
                            "If child is applicant, birthdate here.  Format YYYY-MM-DD",
                            "format":
                            "date-time",
                            "default":
                            None,
                        },
                        "proof_of_identity": {
                            "$ref":
                            "#/definitions/ynexception",
                            "description":
                            "Proof of applicant's identity has been furnished",
                        },
                        "physically_present": {
                            "$ref": "#/definitions/ynexception",
                            "description": "",
                        },
                        "proof_of_residence": {
                            "$ref":
                            "#/definitions/ynexception",
                            "description":
                            "Applicant provided proof of residency within state",
                        },
                        "homeless_residence": {
                            "type":
                            "boolean",
                            "default":
                            False,
                            "description":
                            "Applicant lives in a homeless institution",
                        },
                        "homeless_residence_will_not_benefit": {
                            "type":
                            "boolean",
                            "description":
                            "Homeless facility will not accrue financial benefit",
                            "default":
                            False,
                        },
                        "homeless_residence_foods_will_not_comingle": {
                            "type":
                            "boolean",
                            "description":
                            "Foods provided by WIC will not be co-mingled with homeless facility food",
                            "default":
                            False,
                        },
                        "homeless_residence_does_not_constrain_wic": {
                            "type":
                            "boolean",
                            "description":
                            "Homeless facility does not place constraints on WIC involvement",
                            "default":
                            False,
                        },
                        "currently_pregnant": {
                            "type": "boolean",
                            "description": "",
                            "default": False,
                        },
                        "breastfeeding": {
                            "type": "boolean",
                            "description": "",
                            "default": False,
                        },
                        "date_birth_or_pregnancy_end": {
                            "type": ["string", "null"],
                            "description":
                            "If mother is applicant, birthdate or pregnancy end date here.  Format YYYY-MM-DD",
                            "format":
                            "date-time",
                            "default":
                            None,
                        },
                        "adjunct_income_eligibility": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "program": {
                                        "type": "string",
                                    },
                                    "verified": {
                                        "$ref": "#/definitions/ynexception",
                                    }
                                }
                            }
                        },
                    },
                },
                "income": {
                    "description": "Household income sources",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "dollars": {
                                "type": "number",
                                "multipleOf": 0.01
                            },
                            "frequency": {
                                "type":
                                "string",
                                "enum": [
                                    "annually", "monthly", "semimonthly",
                                    "twice-monthly", "biweekly", "weekly"
                                ]
                            },
                            "source": {
                                "type": "string"
                            },
                            "verified": {
                                "$ref": "#/definitions/ynexception",
                            }
                        }
                    }
                }
            }
        }
    }
}

with open('wic-schema.json', 'w') as outfile:
    json.dump(schema, outfile, indent=2)
