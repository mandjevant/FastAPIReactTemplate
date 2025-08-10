import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export function ConfirmationDialog({
  showConfirmation,
  setShowConfirmation,
  onConfirm,
  item,
  overrideTitle,
  overrideDescription,
}: {
  showConfirmation: boolean;
  setShowConfirmation: (value: boolean) => void;
  onConfirm: (item: any) => void;
  item: any;
  overrideTitle?: string;
  overrideDescription?: React.ReactNode;
}) {
  return (
    <Dialog open={showConfirmation} onOpenChange={setShowConfirmation}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {overrideTitle ? overrideTitle : "Are you sure?"}
          </DialogTitle>
          <DialogDescription asChild>
            <div>
              {overrideDescription
                ? overrideDescription
                : "Do you want to proceed with this action?"}
            </div>
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setShowConfirmation(false)}>
            Cancel
          </Button>
          <Button onClick={() => onConfirm(item)}>Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
