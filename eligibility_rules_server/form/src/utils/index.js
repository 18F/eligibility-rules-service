/* eslint arrow-parens: ["error", "always"] */

const generateRandomInt = () => Math.floor(Math.random() * Math.floor(1000));

const parseAdjunctEligibility = (programs) => {
  if (!programs) return undefined;

  const parsed = Object.keys(programs)
    .map((key) => {
      const program = key.toLowerCase();
      const verified = programs[key];

      if (!verified) return undefined;

      return {
        program,
        verified,
      };
    })
    .filter((i) => i);

  if (parsed.length === 0) return undefined;
  return parsed;
};

const parseApplicant = (arr) => {
  if (!arr || arr.length === 0) return [];

  return arr.map((item) => {
    const { adjunct_income_eligibility, ...attr } = item;
    const programs = parseAdjunctEligibility(adjunct_income_eligibility);

    return {
      id: generateRandomInt(),
      ...attr,
      adjunct_income_eligibility: programs,
    };
  });
};

const parseApplicants = (woman, child) => {
  const women = parseApplicant(woman);
  const children = parseApplicant(child);
  const concated = women.concat(children);

  if (!concated || concated.length === 0) return undefined;

  return concated;
};

const parseEligibilityApplicantForm = (formData) => {
  const { income, woman_applicant, child_applicant, ...other } = formData;

  return [
    {
      application_id: generateRandomInt(),
      applicants: parseApplicants(woman_applicant, child_applicant),
      income,
      ...other,
    },
  ];
};

export default parseEligibilityApplicantForm;
