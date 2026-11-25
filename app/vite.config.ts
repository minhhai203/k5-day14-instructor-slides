import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// GitHub Pages subpath: https://minhhai203.github.io/k5-day14-instructor-slides/
export default defineConfig({
  plugins: [react()],
  base: '/k5-day14-instructor-slides/',
})
