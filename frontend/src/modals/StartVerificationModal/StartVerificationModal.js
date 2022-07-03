import Button from "../../components/atoms/Button/Button";
import Heading from "../../components/atoms/Heading/Heading";
import "./StartVerificationModal.css";

function StartVerificationModal({
  sessionId,
  setShowModal,
  onStartExperiment,
}) {
  const startExperiment = () => {
    setShowModal(false);
    onStartExperiment(sessionId);
  };

  return (
    <div className="verificationContainer">
      <div className="verificationModal">
        <Heading heading={`Are you sure you want to start the experiment?`} />
        <Button
          name={"No"}
          design={"negative"}
          onClick={() => setShowModal(false)}
        />
        <Button
          name={"Yes"}
          design={"positive"}
          onClick={() => startExperiment()}
        />
      </div>
    </div>
  );
}

export default StartVerificationModal;
