import React from 'react';
import Row from '../components/Row';
import ColMd from '../components/ColMd';
import ApplicantForm from '../components/ApplicantForm';
import RequestResult from '../components/RequestResult';

const IndexPage = () => (
  <Row className="py-4">
    <ColMd units={5}>
      <ApplicantForm />
    </ColMd>
    <ColMd units={7}>
      <RequestResult />
    </ColMd>
  </Row>
);

export default IndexPage;
