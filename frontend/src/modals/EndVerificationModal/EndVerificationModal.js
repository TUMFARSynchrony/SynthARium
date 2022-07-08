import Button from "../../components/atoms/Button/Button";
import Heading from "../../components/atoms/Heading/Heading";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";

function EndVerificationModal({ setShowModal, onEndExperiment }) {
  const endExperiment = () => {
    setShowModal(false);
    onEndExperiment();
  };

  return (
    <div className="verificationContainer">
      <div className="verificationModal">
        <Heading heading={`Are you sure you want to end the experiment?`} />
        <Button
          name={"No"}
          design={"negative"}
          onClick={() => setShowModal(false)}
        />
        <LinkButton
          name={"Yes"}
          design={"positive"}
          to="/"
          onClick={() => endExperiment()}
        />
      </div>
    </div>
  );
}

export default EndVerificationModal;
