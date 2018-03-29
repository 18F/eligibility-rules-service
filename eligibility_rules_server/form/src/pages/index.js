import React from 'react';
import Row from '../components/Row';
import ColMd from '../components/ColMd';
import ApplicantForm from '../components/ApplicantForm';

const IndexPage = () => (
  <Row className="py-4">
    <ColMd>
      <ApplicantForm />
    </ColMd>
    <ColMd>Results</ColMd>
  </Row>
);

export default IndexPage;
