const schema = {
  title: 'Eligibility Applicants',
  type: 'object',
  properties: {
    number_in_economic_unit: {
      type: 'number',
      title: 'People in Household',
      default: 1,
      description: 'Number of people in applicant household?',
    },
    physically_present: {
      type: 'string',
      title: 'Are all applicants physically present?',
      enum: ['Yes', 'No', 'Exception'],
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
      items: {
        type: 'object',
        properties: {
          proof_of_identity: {
            type: 'string',
            title: 'Has identity been documented?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          currently_pregnant: {
            type: 'string',
            title: 'Is woman currently pregnant?',
            enum: [true, false],
            enumNames: ['Yes', 'No'],
            default: false,
          },
          breastfeeding: {
            type: 'string',
            title: 'Is woman breastfeeding?',
            enum: [true, false],
            enumNames: ['Yes', 'No'],
            default: false,
          },
          data_birth_or_pregnancy_end: {
            type: 'string',
            format: 'date',
            title: 'Date woman gave birth or pregnancy ended?',
          },
          TANF: {
            type: 'string',
            title:
              'Is woman fully eligible, or presumptively eligible pending completion of the eligibility determination process, to receive Temporary Assistance for Needy Families (TANF)?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          SNAP: {
            type: 'string',
            title: 'Is woman fully eligible to receive SNAP benefits?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Medicaid: {
            type: 'string',
            title: 'Is woman eligible for Medicaid?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          TANF_family: {
            type: 'string',
            title:
              'Is a member of woman’s family certified eligible to receive assistance under TANF?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Medicaid_family: {
            type: 'string',
            title:
              'Is woman a member of family in which a pregnant woman or an infant is certified eligible to receive assistance under Medicaid?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Qualifying_state_plan: {
            type: 'string',
            title:
              'Is woman a participant in a qualifying State-administered program?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
        },
      },
    },
    child_applicant: {
      type: 'array',
      title: 'Add Child',
      items: {
        type: 'object',
        properties: {
          proof_of_identity: {
            type: 'string',
            title: 'Has identity been documented?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
          },
          breastfeeding: {
            type: 'string',
            title: 'Is child breastfeeding?',
            enum: [true, false],
            enumNames: ['Yes', 'No'],
          },
          birthdate: {
            type: 'string',
            format: 'date',
            title: "Child's birthdate",
          },
          TANF: {
            type: 'string',
            title:
              'Is child fully eligible, or presumptively eligible pending completion of the eligibility determination process, to receive Temporary Assistance for Needy Families (TANF)?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          SNAP: {
            type: 'string',
            title: 'Is child fully eligible to receive SNAP benefits?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Medicaid: {
            type: 'string',
            title: 'Is child eligible for Medicaid?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          TANF_family: {
            type: 'string',
            title:
              'Is a member of child’s family certified eligible to receive assistance under TANF?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Medicaid_family: {
            type: 'string',
            title:
              'Is child a member of family in which a pregnant woman or an infant is certified eligible to receive assistance under Medicaid?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
          Qualifying_state_plan: {
            type: 'string',
            title:
              'Is child a participant in a qualifying State-administered program?',
            enum: [true, false, 'exception'],
            enumNames: ['Yes', 'No', 'Exception'],
            default: false,
          },
        },
      },
    },
    income: {
      type: 'array',
      title: 'Add an Income',
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
