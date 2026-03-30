import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          green:  "#37b63a",
          dark:   "#218e28",
          bg:     "#edf3ed",
          bg2:    "#dfe8de",
          text:   "#111611",
          muted:  "#5b655d",
          surface:"#ffffff",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        "2xl": "26px",
        "3xl": "32px",
      },
    },
  },
  plugins: [],
};

export default config;
