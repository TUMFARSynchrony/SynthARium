import ActionButton from "./ActionButton";

const meta = {
  title: "Example/ActionButton",
  component: ActionButton,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {
    backgroundColor: { control: "color" }
  }
};

export default meta;
// type Story = StoryObj<typeof Button>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args

export const Default = () => (
  <ActionButton text={"test"} onClick={() => alert("Button clicked!")}>
    Click me
  </ActionButton>
);

// export const Primary = {
//   // More on args: https://storybook.js.org/docs/react/writing-stories/args
//   args: {
//     label: "ActionButton"
//   }
// };

// export const Secondary = {
//   args: {
//     label: "ActionButton"
//   }
// };

// export const Large = {
//   args: {
//     size: "large",
//     label: "ActionButton"
//   }
// };

// export const Small = {
//   args: {
//     size: "small",
//     label: "ActionButton"
//   }
// };
