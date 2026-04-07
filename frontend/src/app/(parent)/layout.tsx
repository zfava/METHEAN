import Sidebar from "@/components/Sidebar";
import { ChildProvider } from "@/lib/ChildContext";

export default function ParentLayout({ children }: { children: React.ReactNode }) {
  return (
    <ChildProvider>
      <div className="flex min-h-screen bg-(--color-page)">
        <Sidebar />
        <main className="flex-1 px-4 py-4 md:px-8 md:py-6 overflow-y-auto overflow-x-hidden min-h-screen">{children}</main>
      </div>
    </ChildProvider>
  );
}
