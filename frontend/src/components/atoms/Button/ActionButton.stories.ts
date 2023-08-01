import { Meta, StoryObj } from "@storybook/react";
import ActionButton from "./ActionButton";

const meta: Meta<typeof ActionButton> = {
  title: "Example/ActionButton",
  component: ActionButton,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"]
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  // argTypes: {
  //   color: { control: "color" }
  // }
};

export default meta;
type Story = StoryObj<typeof ActionButton>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
export const Primary: Story = {
  // More on args: https://storybook.js.org/docs/react/writing-stories/args
  args: {
    size: "medium",
    text: "Primary Action Button"
  }
};

export const Large: Story = {
  args: {
    size: "large",
    text: "Large Action Button"
  }
};

export const Small: Story = {
  args: {
    size: "small",
    text: "Small Action Button"
  }
};
