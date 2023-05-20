import { ActionButton } from "../../components/atoms/Button";
import Heading from "../../components/atoms/Heading/Heading";
import "./StartVerificationModal.css";

function StartVerificationModal({ setShowModal, onStartExperiment }) {
  const startExperiment = () => {
    setShowModal(false);
    onStartExperiment();
  };

  return (
    <div className="verificationContainer">
      <div className="verificationModal">
        <Heading heading={`Are you sure you want to start the experiment?`} />
        <ActionButton
          text="No"
          variant="contained"
          color="error"
          size="small"
          onClick={() => setShowModal(false)}
        />
        <ActionButton
          text="Yes"
          variant="contained"
          color="success"
          size="small"
          onClick={() => startExperiment()}
        />
      </div>
    </div>
  );
}

export default StartVerificationModal;
