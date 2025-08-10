import { ApiError, UsersService } from "@/client";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { handleError } from "@/utils";
import { useToast } from "@/hooks/use-toast";

export function useDeleteUserMe() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  return useMutation({
    mutationFn: UsersService.deleteUserMe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
    onError: (err: ApiError) => {
      handleError(err, toast);
    },
  });
}

export function useUpdateUserMe() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  return useMutation({
    mutationFn: UsersService.updateUserMe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["company_users"] });
    },
    onError: (err: ApiError) => {
      handleError(err, toast);
    },
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  return useMutation({
    mutationFn: UsersService.updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["company_users"] });
    },
    onError: (err: ApiError) => {
      handleError(err, toast);
    },
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  return useMutation({
    mutationFn: UsersService.deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
    onError: (err: ApiError) => {
      handleError(err, toast);
    },
  });
}
