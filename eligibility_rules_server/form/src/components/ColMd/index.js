import React from 'react';
import PropTypes from 'prop-types';

const ColMd = ({ children, className }) => (
  <div className={`col-md ${className}`}>{children}</div>
);

ColMd.defaultProps = {
  children: null,
  className: '',
};

ColMd.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.array,
    PropTypes.string,
    PropTypes.func,
  ]),
  className: PropTypes.string,
};

export default ColMd;
