import React from 'react';
import PropTypes from 'prop-types';

const ColMd = ({ children, className, units }) => (
  <div className={`col-md-${units} ${className}`}>{children}</div>
);

ColMd.defaultProps = {
  children: null,
  className: '',
  units: 6,
};

ColMd.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.array,
    PropTypes.string,
    PropTypes.func,
  ]),
  className: PropTypes.string,
  units: PropTypes.number,
};

export default ColMd;
