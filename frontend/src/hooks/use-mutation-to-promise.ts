import { UseMutationResult } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";

interface MutationPromiseOptions {
  entityName?: string;
  successMessage?: (itemName?: string) => string;
  errorMessage?: (error: unknown, itemName?: string) => string;
}

export function useMutationToPromise<
  TData = unknown,
  TError = unknown,
  TVariables = void,
  TContext = unknown
>(
  mutation: UseMutationResult<TData, TError, TVariables, TContext>,
  options?: MutationPromiseOptions
) {
  const { toast } = useToast();

  return async (variables: TVariables, itemName?: string) => {
    try {
      const data = await new Promise<TData>((resolve, reject) => {
        mutation.mutate(variables, {
          onSuccess: resolve,
          onError: reject,
        });
      });

      if (options?.successMessage) {
        toast({
          title: `${options.entityName || "Item"} updated successfully`,
          description: options.successMessage(itemName),
        });
      }

      return data;
    } catch (error) {
      const errorMsg = options?.errorMessage
        ? options.errorMessage(error, itemName)
        : error instanceof Error
        ? error.message
        : `Failed to ${
            options?.entityName
              ? `update ${options.entityName.toLowerCase()}`
              : "perform action"
          }`;

      toast({
        variant: "destructive",
        title: `Error ${
          options?.entityName ? `with ${options.entityName}` : ""
        }`,
        description: errorMsg,
      });

      throw error;
    }
  };
}
