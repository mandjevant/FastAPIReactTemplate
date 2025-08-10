import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
} from "@/components/ui/table";
import { perPagePaginationOptions } from "@/utils";
import {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { ConfirmationDialog } from "./ConfirmationDialog";

export type ColumnConfig<T> = {
  key: keyof T;
  label: string;
  type: "text" | "boolean" | "date" | "array" | "number" | "object";
};

type Props<T> = {
  data: T[];
  columns: ColumnConfig<T>[];
  caption: string;
  perPage: number;
  page: number;
  onPerPageChange: (value: number) => void;
  onPageChange: (value: number) => void;
  totalCount: number;
  onEdit?: (item: T) => void;
  onDelete?: (item: T) => void;
};

const formatCell = (value: any, type?: string) => {
  if (type === "date") {
    return new Date(value).toLocaleString();
  }
  if (type === "number") {
    return Number(value).toLocaleString();
  }
  if (type === "boolean") {
    return value ? (
      <span
        role="img"
        aria-label="Yes"
        style={{
          color: "limegreen",
          fontSize: "x-large",
          fontWeight: "bold",
        }}
      >
        ✓
      </span>
    ) : (
      <span role="img" aria-label="No">
        ❌
      </span>
    );
  }
  if (type === "array") {
    return Array.isArray(value)
      ? value.map((item) => JSON.stringify(item)).join(", ")
      : value;
  }
  if (typeof value === "object") {
    return JSON.stringify(value, null, 2);
  }
  return value;
};

export function PaginatedTableLayout<T>({
  data,
  columns,
  caption,
  perPage,
  page,
  onPerPageChange,
  onPageChange,
  totalCount,
  onEdit,
  onDelete,
}: Props<T>) {
  const totalPages = Math.ceil(totalCount / perPage);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<T | null>(null);

  const handleConfirmSubmit = (item) => {
    setShowConfirmation(false);
    onDelete(item);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <div>{caption}</div>
        <Select
          value={perPage.toString()}
          onValueChange={(value) => onPerPageChange(Number(value))}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue>{perPage} row(s) per page</SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              {perPagePaginationOptions.map((option) => (
                <SelectItem key={option} value={option.toString()}>
                  {option}
                </SelectItem>
              ))}
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <Table>
        <TableCaption>{caption}</TableCaption>
        <TableHeader>
          <TableRow>
            {columns.map((col) => (
              <TableHead key={col.key as string}>{col.label}</TableHead>
            ))}
            {(onEdit || onDelete) && (
              <TableHead key="actions">Actions</TableHead>
            )}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item, idx) => (
            <TableRow key={idx}>
              {columns.map((col) => (
                <TableCell key={col.key as string}>
                  {formatCell(item[col.key], col.type)}
                </TableCell>
              ))}
              {(onEdit || onDelete) && (
                <TableCell className="flex space-x-2">
                  {onEdit && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => onEdit(item)}
                    >
                      Edit
                    </Button>
                  )}
                  {onDelete && (
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => {
                        setShowConfirmation(true);
                        setItemToDelete(item);
                      }}
                    >
                      Delete
                    </Button>
                  )}
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <div className="flex items-center justify-between mt-2">
        <p className="text-sm text-muted-foreground">
          Showing {data.length} of {totalCount}
        </p>
        <div className="flex items-center space-x-2">
          <Button
            className="border rounded px-2 py-1"
            disabled={page === 1}
            onClick={() => onPageChange(page - 1)}
          >
            Previous
          </Button>
          <span className="text-sm">
            Page {page} of {totalPages || 1}
          </span>
          <Button
            className="border rounded px-2 py-1"
            disabled={page >= totalPages}
            onClick={() => onPageChange(page + 1)}
          >
            Next
          </Button>
        </div>
      </div>

      <ConfirmationDialog
        showConfirmation={showConfirmation}
        setShowConfirmation={setShowConfirmation}
        onConfirm={handleConfirmSubmit}
        item={itemToDelete}
      />
    </div>
  );
}
