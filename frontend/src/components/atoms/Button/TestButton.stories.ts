import type { Meta, StoryObj } from "@storybook/react";

import { TestButton } from "./TestButton";
// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta: Meta<typeof TestButton> = {
  title: "Example/TestButton",
  component: TestButton,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {
    backgroundColor: { control: "color" }
  }
};

export default meta;
type Story = StoryObj<typeof TestButton>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
export const Primary: Story = {
  // More on args: https://storybook.js.org/docs/react/writing-stories/args
  args: {
    primary: true,
    label: "TestButton"
  }
};

export const Secondary: Story = {
  args: {
    label: "TestButton"
  }
};

export const Large: Story = {
  args: {
    size: "large",
    label: "TestButton"
  }
};

export const Small: Story = {
  args: {
    size: "small",
    label: "TestButton"
  }
};
