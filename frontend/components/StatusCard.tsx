import React from "react";

interface StatusCardProps {
  title: string;
  value: string;
  subValue?: string;
  icon?: React.ReactNode;
  active?: boolean;
}

const StatusCard: React.FC<StatusCardProps> = ({ title, value, subValue, icon, active }) => {
  return (
    <div className="navy-card p-6 flex flex-col justify-between h-32 relative overflow-hidden group hover:border-blue-500/30 transition-all duration-500">
      {/* Subtle indicator for active state */}
      <div className="flex items-center justify-between relative z-10">
        <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest">{title}</h3>
        {icon && <div className="text-blue-400/50 group-hover:text-blue-400 transition-colors">{icon}</div>}
      </div>
      
      <div className="relative z-10">
        <p className={`text-xl font-black ${active ? 'text-emerald-400' : 'text-white'} tracking-tight`}>
          {value}
        </p>
        {subValue && (
          <p className="text-[10px] text-slate-500 font-bold uppercase mt-1 tracking-wider">
            {subValue}
          </p>
        )}
      </div>

      {/* Background glow for active/hover */}
      <div className={`absolute -bottom-4 -right-4 w-24 h-24 bg-blue-600/5 rounded-full blur-2xl group-hover:bg-blue-600/10 transition-all duration-500`} />
    </div>
  );
};

export default StatusCard;
