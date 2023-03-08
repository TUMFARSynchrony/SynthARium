import { ActionButton, LinkActionButton } from "../../components/atoms/Button";
import Heading from "../../components/atoms/Heading/Heading";

function EndVerificationModal({ setShowModal, onEndExperiment }) {
  const endExperiment = () => {
    setShowModal(false);
    onEndExperiment();
  };

  return (
    <div className="verificationContainer">
      <div className="verificationModal">
        <Heading heading={`Are you sure you want to end the experiment?`} />
        <ActionButton
          text="No"
          variant="contained"
          color="error"
          onClick={() => setShowModal(false)}
        />
        <LinkActionButton
          text="Yes"
          path="/"
          variant="contained"
          onClick={() => endExperiment()}
        />
      </div>
    </div>
  );
}

export default EndVerificationModal;
