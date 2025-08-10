import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useState, useEffect } from "react";
import { ConfirmationDialog } from "./ConfirmationDialog";

interface FormFieldPattern {
  value: RegExp;
  message: string;
}

export type FormField<T> = {
  key: keyof T;
  label: string;
  type: "text" | "number" | "boolean" | "date" | "array" | "select" | "json";
  options?: Array<{ label: string; value: string }>;
  placeholder?: string;
  required?: boolean;
  pattern?: FormFieldPattern;
  hidden?: boolean;
};

type FormModalProps<T> = {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: Partial<T>) => void;
  fields: FormField<T>[];
  initialData?: Partial<T>;
  title?: string;
  confirmSubmit?: boolean;
  overruleHidden?: boolean;
};

export function FormModal<T>({
  isOpen,
  onClose,
  onSubmit,
  fields,
  initialData,
  title = "Form",
  confirmSubmit = false,
  overruleHidden = false,
}: FormModalProps<T>) {
  const [formData, setFormData] = useState<Partial<T>>({});
  const [errors, setErrors] = useState<Record<keyof T, string>>(
    {} as Record<keyof T, string>
  );
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [itemToPass, setItemToPass] = useState<Partial<T> | null>(null);

  useEffect(() => {
    setFormData(initialData || {});
    setErrors({} as Record<keyof T, string>);
    setShowConfirmation(false);
  }, [initialData, isOpen]);

  const validateField = (key: keyof T, value: any): string => {
    const field = fields.find((f) => f.key === key);
    if (!field) return "";

    if (field.type === "boolean" || field.type === "date") return "";

    if (field.required) {
      if (value === null || value === undefined || value === "") {
        return "This field is required.";
      }
    }

    if (field.type === "json" || field.type === "array") {
      try {
        if (value && value.trim() !== "") {
          JSON.parse(value);
        }
      } catch (e) {
        return "Invalid JSON format";
      }
    }

    if (value && field.pattern && !field.pattern.value.test(String(value))) {
      return field.pattern.message;
    }

    return "";
  };

  const handleChange = (key: keyof T, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));

    const error = validateField(key, value);
    setErrors((prev) => ({ ...prev, [key]: error }));
  };

  const handleSubmit = () => {
    const newErrors: Record<keyof T, string> = {} as Record<keyof T, string>;
    let hasErrors = false;
    const processedData = { ...formData };

    for (const field of fields) {
      const value = formData[field.key];
      const error = validateField(field.key, value);

      if (
        (field.type === "json" || field.type === "array") &&
        value &&
        typeof value === "string"
      ) {
        try {
          processedData[field.key] = JSON.parse(value as string);
        } catch (e) {
          hasErrors = true;
          newErrors[field.key] = "Invalid JSON format";
        }
      }

      if (error) {
        hasErrors = true;
        newErrors[field.key] = error;
      }
    }

    setErrors(newErrors);

    if (!hasErrors) {
      setItemToPass(processedData);
      if (confirmSubmit) {
        setShowConfirmation(true);
      } else {
        onSubmit(processedData);
        onClose();
      }
    }
  };

  const handleConfirmSubmit = (item: Partial<T>) => {
    onSubmit(item);
    setShowConfirmation(false);
    onClose();
  };

  return (
    <>
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {fields.map(
              (field) =>
                (!field.hidden || overruleHidden) && (
                  <div key={field.key as string}>
                    <Label>{field.label}</Label>
                    {field.type === "boolean" ? (
                      <Input
                        type="checkbox"
                        checked={!!formData[field.key]}
                        onChange={(e) =>
                          handleChange(field.key, e.target.checked)
                        }
                      />
                    ) : field.type === "select" ? (
                      <select
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        value={(formData[field.key] as string) ?? ""}
                        onChange={(e) =>
                          handleChange(field.key, e.target.value)
                        }
                      >
                        <option value="">
                          {field.placeholder || "Select an option"}
                        </option>
                        {field.options?.map((option, index) => (
                          <option key={index} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    ) : (
                      <Input
                        type={
                          field.type === "date"
                            ? "date"
                            : field.type === "number"
                            ? "number"
                            : "text"
                        }
                        placeholder={field.placeholder ?? ""}
                        value={(formData[field.key] as any) ?? ""}
                        onChange={(e) =>
                          handleChange(field.key, e.target.value)
                        }
                      />
                    )}
                    {field.type === "array" && (
                      <p className="text-xs text-muted-foreground mt-1">
                        Enter as JSON array: ["feature 1", "feature 2"]
                      </p>
                    )}
                    {errors[field.key] && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors[field.key]}
                      </p>
                    )}
                  </div>
                )
            )}
            <div className="flex justify-end space-x-2 pt-4">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button onClick={handleSubmit}>Submit</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ConfirmationDialog
        showConfirmation={showConfirmation}
        setShowConfirmation={setShowConfirmation}
        onConfirm={handleConfirmSubmit}
        item={itemToPass}
      />
    </>
  );
}
