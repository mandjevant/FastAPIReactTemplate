import { useState, useEffect } from "react";
import { useQuery, UseQueryOptions } from "@tanstack/react-query";
import {
  PaginatedTableLayout,
  ColumnConfig,
} from "@/components/ux/PaginatedTableLayout";
import { useToast } from "@/hooks/use-toast";
import { FormModal, FormField } from "@/components/ux/FormModal";

interface CrudTableProps<T extends Record<string, any>, U = Partial<T>> {
  columns: ColumnConfig<T>[];
  queryOptions: (params: {
    page: number;
    rowsPerPage: number;
  }) => UseQueryOptions<any>;
  formFields: FormField<T>[];
  deleteMutation: (item: T) => Promise<any>;
  updateMutation: (row: Partial<T>, data: U) => Promise<any>;
  title: string;
  initialData?: Partial<T>;
}

export function CrudTable<T extends Record<string, any>, U = Partial<T>>({
  columns,
  queryOptions,
  formFields,
  deleteMutation,
  updateMutation,
  title,
  initialData = {},
}: CrudTableProps<T, U>) {
  const [perPage, setPerPage] = useState(10);
  const [page, setPage] = useState(1);
  const [formOpen, setFormOpen] = useState(false);
  const [editData, setEditData] = useState<Partial<T> | null>(null);
  const { toast } = useToast();

  const { data } = useQuery({
    ...queryOptions({ page, rowsPerPage: perPage }),
    placeholderData: (prev) => prev,
  });

  const handleEdit = (item: T) => {
    setEditData(item);
    setFormOpen(true);
  };

  const handleDelete = async (item: T) => {
    try {
      await deleteMutation(item);
      toast({
        title: `${title} deleted`,
        description: `${title} ${item.name || item.id} has been deleted.`,
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: `Error deleting ${title.toLowerCase()}`,
        description: error.message,
      });
    }
  };

  const handleFormSubmit = async (data: Partial<T>) => {
    try {
      if (editData?.id) {
        await updateMutation(editData, data as U);
        toast({
          title: `${title} updated`,
          description: `${title} ${data.name || data.id} has been updated.`,
        });
      }
      setFormOpen(false);
      setEditData(null);
    } catch (error) {
      toast({
        variant: "destructive",
        title: `Error updating ${title.toLowerCase()}`,
        description: error.message,
      });
    }
  };

  useEffect(() => {
    setPage(1);
  }, [perPage]);

  return (
    <>
      <PaginatedTableLayout
        data={data?.data ?? []}
        columns={columns}
        caption={`${
          title.endsWith("y") ? title.slice(0, -1) + "ie" : title
        }s (${data?.count ?? 0})`}
        perPage={perPage}
        onPerPageChange={setPerPage}
        totalCount={data?.count ?? 0}
        page={page}
        onPageChange={setPage}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <FormModal<T>
        isOpen={formOpen}
        onClose={() => {
          setEditData(null);
          setFormOpen(false);
        }}
        onSubmit={handleFormSubmit}
        fields={formFields}
        initialData={editData ?? initialData}
        title={`Edit ${title}`}
      />
    </>
  );
}
