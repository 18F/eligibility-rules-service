import React from 'react';
import PropTypes from 'prop-types';
import htmlescape from 'htmlescape';
import api from '../../api';
import ColMd from '../../components/ColMd';
import Row from '../../components/Row';
import parseEligibilityApplicantForm from '../../utils';

const Form = (FormComponent, ResultComponent) => {
  class FormContainer extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        result: '',
      };

      this.onSubmitHandler = this.onSubmitHandler.bind(this);
    }

    onSubmitHandler(payload) {
      const { formData } = payload;
      const parsed = parseEligibilityApplicantForm(formData);

      api(parsed)
        .then((res) => {
          this.setState({
            result: JSON.stringify(res, null, 2),
          });
        })
        .catch((err) => {
          this.setState({
            result: JSON.stringify(err, null, 2),
          });
        });
    }

    render() {
      return (
        <Row className="py-4">
          <ColMd units={5}>
            <FormComponent submit={this.onSubmitHandler} />
          </ColMd>
          <ColMd units={7}>
            <ResultComponent result={this.state.result} />
          </ColMd>
        </Row>
      );
    }
  }

  return <FormContainer />;
};

Form.defaultProps = {
  post: () => {},
};

Form.propTypes = {
  post: PropTypes.func,
};

export default Form;
