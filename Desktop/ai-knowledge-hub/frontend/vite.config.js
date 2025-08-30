import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// Adjust backend target/ports if needed:
const BACKEND = process.env.BACKEND_URL || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      // REST API (Django DRF)
      "/api": {
        target: BACKEND,
        changeOrigin: true
      },
      // Socket.IO proxy: expose /socket.io locally -> backend /ws/socket.io
      "/socket.io": {
        target: BACKEND,
        ws: true,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/socket\.io/, "/ws/socket.io")
      },
      // Admin (optional, handy during dev)
      "/admin": {
        target: BACKEND,
        changeOrigin: true
      },
      // Media/static passthrough for local dev (optional)
      "/media": {
        target: BACKEND,
        changeOrigin: true
      },
      "/static": {
        target: BACKEND,
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    chunkSizeWarningLimit: 900
  },
  resolve: {
    alias: {
      "@": "/src"
    }
  }
});
