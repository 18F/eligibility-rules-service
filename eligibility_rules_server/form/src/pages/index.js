import ApplicantForm from '../components/ApplicantForm';
import RequestResult from '../components/RequestResult';
import Form from '../containers/Form';

const ContainerForm = Form(ApplicantForm, RequestResult);

const IndexPage = () => ContainerForm;

export default IndexPage;
