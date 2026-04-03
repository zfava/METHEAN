import Sidebar from "@/components/Sidebar";
import { ChildProvider } from "@/lib/ChildContext";

export default function ParentLayout({ children }: { children: React.ReactNode }) {
  return (
    <ChildProvider>
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 p-8 overflow-y-auto">{children}</main>
      </div>
    </ChildProvider>
  );
}
