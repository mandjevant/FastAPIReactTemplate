import * as React from "react";

interface ColorPickerProps {
  value?: string;
  onChange?: (value: string) => void;
}

export const ColorPicker: React.FC<ColorPickerProps> = ({
  value = "#000000",
  onChange,
}) => {
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.value);
  };

  return (
    <div
      onClick={handleClick}
      className="relative h-8 w-8 cursor-pointer rounded-md border border-input shadow-sm"
      style={{ backgroundColor: value }}
    >
      <input
        ref={inputRef}
        type="color"
        value={value}
        onChange={handleChange}
        className="absolute inset-0 h-full w-full opacity-0 cursor-pointer"
      />
    </div>
  );
};
