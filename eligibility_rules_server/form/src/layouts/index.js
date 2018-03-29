import React from 'react';
import PropTypes from 'prop-types';
import Helmet from 'react-helmet';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import Container from '../components/Container';
import Header from '../components/Header';

const TemplateWrapper = ({ children, data }) => (
  <div>
    <Helmet
      title={data.site.siteMetadata.title}
      meta={[
        { name: 'description', content: data.site.siteMetadata.description },
        { name: 'keywords', content: data.site.siteMetadata.keywords },
      ]}
    />
    <Container>
      <Header />
      {children()}
    </Container>
  </div>
);

TemplateWrapper.defaultProps = {
  children: null,
  data: null,
};

TemplateWrapper.propTypes = {
  children: PropTypes.func,
  data: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    keywords: PropTypes.string,
  }),
};

export default TemplateWrapper;

export const layoutQuery = graphql`
  query LayoutQuery {
    site {
      siteMetadata {
        title
        description
      }
    }
  }
`;
