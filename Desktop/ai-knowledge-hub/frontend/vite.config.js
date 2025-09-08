import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

const BACKEND = process.env.BACKEND_URL || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        target: BACKEND,
        changeOrigin: true,
      },
      "/socket.io": {
        target: BACKEND,
        ws: true,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/socket\.io/, "/ws/socket.io"),
      },
      "/admin": {
        target: BACKEND,
        changeOrigin: true,
      },
      "/media": {
        target: BACKEND,
        changeOrigin: true,
      },
      "/static": {
        target: BACKEND,
        changeOrigin: true,
      },
    },
    // 👇 This is the important part
    fs: {
      allow: ["."],
    },
    historyApiFallback: true, // ensures React Router works on refresh
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    chunkSizeWarningLimit: 900,
  },
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
