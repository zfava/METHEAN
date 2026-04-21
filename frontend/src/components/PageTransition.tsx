"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import { useMobile } from "@/lib/useMobile";

function segmentCount(path: string): number {
  return path.split("/").filter(Boolean).length;
}

export default function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isMobile = useMobile();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [state, setState] = useState<"idle" | "exiting" | "entering">("idle");
  const [direction, setDirection] = useState<"left" | "right" | "fade">("fade");
  const prevPathname = useRef(pathname);
  const prevDepth = useRef(segmentCount(pathname));

  useEffect(() => {
    if (pathname !== prevPathname.current) {
      const newDepth = segmentCount(pathname);
      const oldDepth = prevDepth.current;

      if (isMobile) {
        if (newDepth > oldDepth) setDirection("left");
        else if (newDepth < oldDepth) setDirection("right");
        else setDirection("fade");
      } else {
        setDirection("fade");
      }

      setState("exiting");
      const timer = setTimeout(() => {
        setDisplayChildren(children);
        setState("entering");
        prevPathname.current = pathname;
        prevDepth.current = newDepth;
        const enterTimer = setTimeout(() => setState("idle"), 200);
        return () => clearTimeout(enterTimer);
      }, 150);
      return () => clearTimeout(timer);
    } else {
      setDisplayChildren(children);
    }
  }, [pathname, children, isMobile]);

  const getStyle = (): React.CSSProperties => {
    const spring = "cubic-bezier(0.32, 0.72, 0, 1)";

    if (state === "exiting") {
      if (direction === "left") {
        return { opacity: 0, transform: "translateX(-24px)", transition: `opacity 0.15s ${spring}, transform 0.15s ${spring}` };
      }
      if (direction === "right") {
        return { opacity: 0, transform: "translateX(24px)", transition: `opacity 0.15s ${spring}, transform 0.15s ${spring}` };
      }
      return { opacity: 0, transform: "translateY(4px)", transition: `opacity 0.15s ${spring}, transform 0.15s ${spring}` };
    }

    if (state === "entering") {
      if (direction === "left") {
        return { opacity: 1, transform: "translateX(0)", transition: `opacity 0.2s ${spring}, transform 0.2s ${spring}` };
      }
      if (direction === "right") {
        return { opacity: 1, transform: "translateX(0)", transition: `opacity 0.2s ${spring}, transform 0.2s ${spring}` };
      }
      return { opacity: 1, transform: "translateY(0)", transition: `opacity 0.2s ${spring}, transform 0.2s ${spring}` };
    }

    return { opacity: 1, transform: "translateX(0) translateY(0)", willChange: "auto" };
  };

  return (
    <div style={getStyle()}>
      {displayChildren}
    </div>
  );
}
