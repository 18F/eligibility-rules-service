const schema = {
  title: 'Eligibility Applicants',
  type: 'object',
  required: [
    'number_in_economic_unit',
    'all_applicants_present',
    'referrer_state',
  ],
  properties: {
    number_in_economic_unit: {
      type: 'number',
      title: 'People in Household',
      default: 1,
      description: 'Number of people in applicant household?',
    },
    all_applicants_present: {
      type: 'string',
      title: 'Are all applicants physically present?',
      enum: ['true', 'false', 'exception'],
      enumNames: ['Yes', 'No', 'Exception'],
      default: 'false',
    },
    referrer_state: {
      type: 'string',
      title: 'State',
      enum: ['AK', 'AZ', 'HI', 'NJ'],
      enumNames: ['Alaska', 'Arizona', 'Hawaii', 'New Jersey'],
    },
    woman_applicant: {
      type: 'array',
      title: 'Add Woman',
      required: ['physically_present', 'proof_of_identity'],
      items: {
        type: 'object',
        properties: {
          proof_of_identity: {
            type: 'string',
            title: 'Has identity been documented?',
            enum: ['true', 'false', 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: 'false',
          },
          physically_present: {
            type: 'boolean',
            title: 'Applicant is physically present?',
          },
          proof_of_residence: {
            type: 'boolean',
            title: 'Applicant has proof of residence?',
          },
          homeless_residence: {
            type: 'boolean',
            title: 'Applicant is homeless?',
            default: false,
          },
          currently_pregnant: {
            type: 'boolean',
            title: 'Is woman currently pregnant?',
          },
          breastfeeding: {
            type: 'boolean',
            title: 'Is woman breastfeeding?',
          },
          data_birth_or_pregnancy_end: {
            type: 'string',
            format: 'date',
            title: 'Date woman gave birth or pregnancy ended?',
          },
          adjunct_income_eligibility: {
            title: 'Eligibility Programs',
            type: 'object',
            properties: {
              TANF: {
                type: 'string',
                title:
                  'Is woman fully eligible, or presumptively eligible pending completion of the eligibility determination process, to receive Temporary Assistance for Needy Families (TANF)?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              SNAP: {
                type: 'string',
                title: 'Is woman fully eligible to receive SNAP benefits?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Medicaid: {
                type: 'string',
                title: 'Is woman eligible for Medicaid?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              TANF_family: {
                type: 'string',
                title:
                  'Is a member of woman’s family certified eligible to receive assistance under TANF?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Medicaid_family: {
                type: 'string',
                title:
                  'Is woman a member of family in which a pregnant woman or an infant is certified eligible to receive assistance under Medicaid?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Qualifying_state_plan: {
                type: 'string',
                title:
                  'Is woman a participant in a qualifying State-administered program?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
            },
          },
        },
      },
    },
    child_applicant: {
      type: 'array',
      title: 'Add Child',
      required: ['physically_present', 'proof_of_identity'],
      items: {
        type: 'object',
        properties: {
          proof_of_identity: {
            type: 'string',
            title: 'Has identity been documented?',
            enum: ['true', 'false', 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
          },
          physically_present: {
            type: 'boolean',
            title: 'Applicant is physically present?',
          },
          proof_of_residence: {
            type: 'boolean',
            title: 'Applicant has proof of residence?',
          },
          homeless_residence: {
            type: 'boolean',
            title: 'Applicant is homeless?',
            default: false,
          },
          breastfeeding: {
            type: 'boolean',
            title: 'Is child breastfeeding?',
          },
          birthdate: {
            type: 'string',
            format: 'date',
            title: "Child's birth date",
          },
          adjunct_income_eligibility: {
            title: 'Eligibility Programs',
            type: 'object',
            properties: {
              TANF: {
                type: 'string',
                title:
                  'Is child fully eligible, or presumptively eligible pending completion of the eligibility determination process, to receive Temporary Assistance for Needy Families (TANF)?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              SNAP: {
                type: 'string',
                title: 'Is child fully eligible to receive SNAP benefits?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Medicaid: {
                type: 'string',
                title: 'Is child eligible for Medicaid?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              TANF_family: {
                type: 'string',
                title:
                  'Is a member of child’s family certified eligible to receive assistance under TANF?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Medicaid_family: {
                type: 'string',
                title:
                  'Is child a member of family in which a pregnant woman or an infant is certified eligible to receive assistance under Medicaid?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
              Qualifying_state_plan: {
                type: 'string',
                title:
                  'Is child a participant in a qualifying State-administered program?',
                enum: ['true', 'false', 'exception'],
                enumNames: ['Yes', 'No', 'Exception'],
              },
            },
          },
        },
      },
    },
    income: {
      type: 'array',
      title: 'Add an Income',
      required: ['dollars', 'source', 'frequency', 'verified'],
      items: {
        type: 'object',
        properties: {
          dollars: {
            type: 'number',
            title: 'Income Amount',
          },
          source: {
            type: 'string',
            title: 'Income Source',
            enum: [
              'wages-and-salary',
              'self-employment',
              'social-security',
              'royalties',
              'alimony-and-child-support',
            ],
            enumNames: [
              'Wages and salary',
              'Self-employment',
              'Social security',
              'Royalties',
              'Alimony and child support',
            ],
          },
          frequency: {
            type: 'string',
            title: 'Income Frequency',
            enum: [
              'weekly',
              'bi-weekly',
              'semi-monthly',
              'monthly',
              'annually',
            ],
            enumNames: [
              'Weekly',
              'Bi-weekly',
              'Semi-monthly',
              'Monthly',
              'Annually',
            ],
          },
          verified: {
            type: 'boolean',
            title: 'Verified?',
            default: false,
          },
        },
      },
    },
  },
};

export default schema;

export const uiSchema = {
  applicants: {
    items: {
      'ui:widget': 'id',
    },
  },
};
