import React from 'react';
import PropTypes from 'prop-types';
import Form from 'react-jsonschema-form';
import schema from '../../constants/applicantSchema';

const ApplicantForm = ({ change, error, submit }) => (
  <Form schema={schema} onChange={change} onSubmit={submit} onError={error} />
);

ApplicantForm.defaultProps = {
  change: () => {},
  error: () => {},
  submit: () => {},
};

ApplicantForm.propTypes = {
  change: PropTypes.func,
  error: PropTypes.func,
  submit: PropTypes.func,
};

export default ApplicantForm;
