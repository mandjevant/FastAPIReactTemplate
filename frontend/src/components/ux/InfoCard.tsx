import React from "react";
import { AlertCircle } from "lucide-react";

interface InfoCardProps {
  title: string;
  message: string;
  icon?: React.ReactNode;
}

const InfoCard: React.FC<InfoCardProps> = ({ title, message, icon }) => {
  return (
    <div className="relative z-10 w-full max-w-md rounded-md bg-card p-8 shadow-xl space-y-4 text-center border">
      <div className="flex justify-center">
        {icon ?? <AlertCircle className="w-10 h-10 text-blue-600" />}
      </div>
      <h2 className="text-xl font-semibold">{title}</h2>
      <p className="text-sm text-muted-foreground">{message}</p>
    </div>
  );
};

export default InfoCard;
