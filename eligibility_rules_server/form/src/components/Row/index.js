import React from 'react';
import PropTypes from 'prop-types';

const Row = ({ children, className }) => (
  <div className={`row ${className}`}>{children}</div>
);

Row.defaultProps = {
  children: null,
  className: '',
};

Row.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.array,
    PropTypes.string,
    PropTypes.func,
  ]),
  className: PropTypes.string,
};

export default Row;
