import React from 'react';
import PropTypes from 'prop-types';

const RequestResult = ({ result }) => (
  <div className="rjsf">
    <legend>Result</legend>
    <pre>{result}</pre>
  </div>
);

RequestResult.defaultProps = {
  result: '',
};

RequestResult.propTypes = {
  result: PropTypes.string,
};

export default RequestResult;
