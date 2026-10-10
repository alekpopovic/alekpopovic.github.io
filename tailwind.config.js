module.exports = {
  content: [
    "./*.html",
    "./_layouts/**/*.html",
    "./_includes/**/*.html",
    "./book-pages/**/*.html",
    "./_posts/**/*.md"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#20201e",
        moss: "#535247",
        fern: "#2864ff",
        clay: "#fd4401",
        paper: "#fff3b8",
        pearl: "#ffd33d"
      },
      fontFamily: {
        sans: ["DM Sans", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Passion One", "Arial Black", "sans-serif"]
      },
      boxShadow: {
        soft: "0 18px 60px rgba(23, 33, 29, 0.12)"
      }
    }
  },
  plugins: [
    require("@tailwindcss/typography")
  ]
};
