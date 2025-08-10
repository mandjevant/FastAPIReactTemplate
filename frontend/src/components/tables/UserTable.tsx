import { UserPublic, UserUpdate } from "@/client";
import { ColumnConfig } from "@/components/ux/PaginatedTableLayout";
import { getUsersQueryOptions } from "@/queries/users";
import { FormField } from "../ux/FormModal";
import { emailPattern, phonePattern } from "@/utils";
import { useMutationToPromise } from "@/hooks/use-mutation-to-promise";
import { useDeleteUser, useUpdateUser } from "@/mutations/users";
import { CrudTable } from "../ux/CrudTable";

const columns: ColumnConfig<UserPublic>[] = [
  { key: "email", label: "Email", type: "text" },
  { key: "full_name", label: "Full Name", type: "text" },
  { key: "is_active", label: "Active", type: "boolean" },
  { key: "is_superuser", label: "Admin", type: "boolean" },
  { key: "id", label: "ID", type: "text" },
  { key: "created_at", label: "Created", type: "date" },
  { key: "updated_at", label: "Updated", type: "date" },
];

const fields: FormField<UserUpdate>[] = [
  {
    key: "email",
    label: "Email",
    type: "text",
    pattern: emailPattern,
  },
  {
    key: "full_name",
    label: "Full Name",
    type: "text",
  },
  {
    key: "avatar_url",
    label: "Avatar URL",
    type: "text",
  },
  {
    key: "phone",
    label: "Phone",
    type: "text",
    pattern: phonePattern,
  },
  {
    key: "password",
    label: "Password",
    type: "text",
  },
  {
    key: "is_active",
    label: "Active",
    type: "boolean",
  },
  {
    key: "is_superuser",
    label: "Admin",
    type: "boolean",
  },
];

const UserTable = () => {
  const updateMutation = useMutationToPromise(useUpdateUser(), {
    entityName: "User",
    successMessage: (name) => `User ${name || ""} was updated successfully`,
    errorMessage: (error, name) =>
      `Failed to update ${name ? `user ${name}` : "user"}: ${
        error instanceof Error ? error.message : "Unknown error"
      }`,
  });
  const deleteMutation = useMutationToPromise(useDeleteUser(), {
    entityName: "user",
    successMessage: (name) => `User ${name || ""} was deleted successfully`,
  });

  return (
    <CrudTable<UserPublic, UserUpdate>
      columns={columns}
      queryOptions={getUsersQueryOptions}
      formFields={fields}
      deleteMutation={(user) =>
        deleteMutation({ userId: user.id }, user.full_name)
      }
      updateMutation={(row, data) =>
        updateMutation({ userId: row.id, requestBody: data }, data.full_name)
      }
      title="User"
    />
  );
};

export default UserTable;
