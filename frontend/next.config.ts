import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: process.env.CAP_BUILD === "true" ? "export" : "standalone",
};

export default nextConfig;
