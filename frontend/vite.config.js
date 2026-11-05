import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, /api is proxied to Django. In production the reverse proxy (Nginx/Ingress)
// must do the same routing: that wiring is a DevOps responsibility.
export default defineConfig({
  plugins: [react()],
  server: { port: 3000, proxy: { "/api": "http://localhost:8000" } },
});
