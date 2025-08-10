import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm, type SubmitHandler } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import useAuth from "@/hooks/use-auth";
import { useToast } from "@/hooks/use-toast";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/home/Footer";
import useIsLoggedIn from "@/hooks/use-is-loggedin";
import { emailPattern, passwordRules } from "@/utils";
import RecoverPassword from "@/components/auth/RecoverPassword";

interface LoginForm {
  email: string;
  password: string;
}

export default function Login() {
  const { loginMutation } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const isLoggedIn = useIsLoggedIn();

  if (isLoggedIn) {
    navigate("/dashboard");
  }

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    mode: "onBlur",
  });

  const onSubmit: SubmitHandler<LoginForm> = (data) => {
    loginMutation.mutate(
      {
        username: data.email,
        password: data.password,
      },
      {
        onSuccess: () => {
          toast({
            title: "Success",
            description: "Logged in successfully",
          });
        },
        onError: () => {
          toast({
            variant: "destructive",
            title: "Error",
            description: "Invalid credentials",
          });
        },
      }
    );
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-1">
        {/* Right side form */}
        <div className="flex items-center justify-center p-8">
          <div className="w-full max-w-sm rounded-md space-y-8 p-8 shadow-xl">
            {/* <div className="w-full max-w-sm space-y-8"> */}
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold tracking-tight">
                Welcome back
              </h1>
              <p className="text-muted-foreground">Sign in to your account</p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  {...register("email", {
                    required: "Email is required",
                    pattern: emailPattern,
                  })}
                  disabled={isSubmitting}
                />
                {errors.email && (
                  <p className="text-sm text-red-500">{errors.email.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  {...register("password", passwordRules())}
                  placeholder="Password"
                  disabled={isSubmitting}
                />
                {errors.password && (
                  <p className="text-sm text-red-500">
                    {errors.password.message}
                  </p>
                )}
              </div>

              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting && (
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                )}
                Sign In
              </Button>
            </form>

            <div className="text-center text-sm space-y-3">
              <RecoverPassword />
              <div>
                Don't have an account?{" "}
                <Button
                  variant="link"
                  className="text-primary font-semibold px-0"
                  onClick={() => navigate("/auth/signup")}
                >
                  Sign up
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
