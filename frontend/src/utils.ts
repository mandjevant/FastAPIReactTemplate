import type { ApiError } from "./client";
import { useToast } from "@/hooks/use-toast";

export const userRolePattern: { value: RegExp; message: string } = {
  value: /^(owner|admin|member|guest)$/,
  message: "Invalid user role. Must be `owner`, `admin`, `member` or `guest`.",
};

export const phonePattern: { value: RegExp; message: string } = {
  value: /^\+?[1-9]\d{1,14}$/, // E.164 format
  message: "Invalid phone number",
};

export const urlPattern: { value: RegExp; message: string } = {
  value: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/,
  message: "Invalid URL",
};

export const addressPattern: { value: RegExp; message: string } = {
  value: /^[A-Za-z0-9\s,.'-]{3,}$/, // Basic address validation
  message: "Invalid address",
};

export const postcodePattern: { value: RegExp; message: string } = {
  value: /^\d{5}(-\d{4})?$/, // US ZIP code format
  message: "Invalid postcode",
};

export const perPagePaginationOptions: number[] = [1, 5, 10, 25, 50, 100];

export const uuidPattern: { value: RegExp; message: string } = {
  value: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
  message: "Invalid UUID",
};

export const emailPattern: { value: RegExp; message: string } = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
};

export const namePattern: { value: RegExp; message: string } = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Invalid name",
};

export const passwordPattern: { value: RegExp; message: string } = {
  value: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/, // Minimum 8 characters, at least one letter and one number
  message:
    "Password must be at least 8 characters long and include at least one letter and one number",
};

export const passwordRules = (isRequired: boolean = true): any => {
  const rules: any = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  };

  if (isRequired) {
    rules.required = "Password is required";
  }

  return rules;
};

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password;
      return value === password ? true : "The passwords do not match";
    },
  };

  if (isRequired) {
    rules.required = "Password confirmation is required";
  }

  return rules;
};

export const handleError = (
  err: ApiError,
  toast: ReturnType<typeof useToast>["toast"]
) => {
  const errDetail = (err.body as any)?.detail;
  let errorMessage = errDetail || "Something went wrong.";
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    errorMessage = errDetail[0].msg;
  }
  toast({
    variant: "destructive",
    title: "Error",
    description: errorMessage,
  });
};
