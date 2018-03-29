import React from 'react';
import Link from 'gatsby-link';

const Header = () => (
  <nav className="navbar navbar-expand-lg navbar-light py-4">
    <Link to="/">
      <span className="navbar-brand mb-0 h1">Eligibility Rules Service</span>
      <span className="navbar-text">Example Form</span>
    </Link>
  </nav>
);

export default Header;
