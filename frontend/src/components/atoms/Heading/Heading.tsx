import "./Heading.css";

type HeadingProps = {
  heading: string;
};

function Heading({ heading }: HeadingProps) {
  return <h2 className="heading">{heading}</h2>;
}

export default Heading;
