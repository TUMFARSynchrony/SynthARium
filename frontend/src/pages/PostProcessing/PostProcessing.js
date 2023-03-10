import HeroText from "../../components/atoms/HeroText/HeroText";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";

function PostProcessing() {
  return (
    <>
      <NavigationBar />
      <HeroText text={"Post-Processing Room"} />
      <HeroText text={"Under construction! This is the page where you can analyze and visualize the experiment data after conducting your experiment."} />
    </>
  );
}

export default PostProcessing;
