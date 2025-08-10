import { UsersService } from "@/client";

export function getUsersQueryOptions({
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
}) {
  return {
    queryFn: () =>
      UsersService.listUsers({
        skip: (page - 1) * rowsPerPage,
        limit: rowsPerPage,
      }),
    queryKey: ["users", { page, rowsPerPage }],
  };
}

export function getReadUserQueryOptions({ userId }: { userId: string }) {
  return {
    queryFn: () => UsersService.readUser({ userId }),
    queryKey: ["user", userId],
    enabled: !!userId,
  };
}
