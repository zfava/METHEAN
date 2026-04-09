import { useEffect, useState } from "react";

export function useStagger(itemCount: number, delayMs: number = 50): boolean[] {
  const [visible, setVisible] = useState<boolean[]>(new Array(itemCount).fill(false));

  useEffect(() => {
    const timers: NodeJS.Timeout[] = [];
    for (let i = 0; i < itemCount; i++) {
      timers.push(setTimeout(() => {
        setVisible((prev) => {
          const next = [...prev];
          next[i] = true;
          return next;
        });
      }, i * delayMs));
    }
    return () => timers.forEach(clearTimeout);
  }, [itemCount, delayMs]);

  return visible;
}
