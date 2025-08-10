import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm, type SubmitHandler } from "react-hook-form";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";
import useAuth from "@/hooks/use-auth";
import type { UserRegister } from "@/client";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/home/Footer";
import {
  emailPattern,
  namePattern,
  passwordRules,
  confirmPasswordRules,
} from "@/utils";

interface UserRegisterForm extends UserRegister {
  confirm_password: string;
}

export default function SignUp() {
  const { signUpMutation } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors, isSubmitting },
  } = useForm<UserRegisterForm>({
    mode: "onBlur",
  });

  const onSubmit: SubmitHandler<UserRegisterForm> = (data) => {
    if (data.password !== data.confirm_password) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Passwords do not match",
      });
      return;
    }

    signUpMutation.mutate(data, {
      onSuccess: () => {
        toast({
          title: "Account created",
          description: "You can now log in.",
        });
      },
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-1">
        <div className="flex items-center justify-center p-8">
          <div className="w-full max-w-sm space-y-6 rounded-md p-8 shadow-xl">
            <div className="text-center space-y-2">
              <h1 className="text-2xl font-semibold">Create an account</h1>
            </div>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid gap-2">
                <Label htmlFor="full_name">Full Name</Label>
                <Input
                  id="full_name"
                  type="text"
                  placeholder="John Doe"
                  {...register("full_name", {
                    required: "Full name is required",
                    pattern: namePattern,
                  })}
                  disabled={isSubmitting}
                />
                {errors.full_name && (
                  <p className="text-sm text-red-500 mt-1">
                    {errors.full_name.message}
                  </p>
                )}
              </div>
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="name@example.com"
                  {...register("email", {
                    required: "Email is required",
                    pattern: emailPattern,
                  })}
                  disabled={isSubmitting}
                />
                {errors.email && (
                  <p className="text-sm text-red-500 mt-1">
                    {errors.email.message}
                  </p>
                )}
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  {...register("password", passwordRules())}
                  disabled={isSubmitting}
                />
                {errors.password && (
                  <p className="text-sm text-red-500 mt-1">
                    {errors.password.message}
                  </p>
                )}
              </div>
              <div className="grid gap-2">
                <Label htmlFor="confirm_password">Confirm Password</Label>
                <Input
                  id="confirm_password"
                  type="password"
                  {...register(
                    "confirm_password",
                    confirmPasswordRules(getValues)
                  )}
                  disabled={isSubmitting}
                />
                {errors.confirm_password && (
                  <p className="text-sm text-red-500 mt-1">
                    {errors.confirm_password.message}
                  </p>
                )}
              </div>
              <Button className="w-full" type="submit" disabled={isSubmitting}>
                {isSubmitting && <div className="mr-2 h-4 w-4 animate-spin" />}
                Sign Up
              </Button>
            </form>
            <div className="text-center text-sm">
              Already have an account?{" "}
              <button
                onClick={() => navigate("/auth/login")}
                className="text-primary underline"
              >
                Log In
              </button>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
