module.exports = {
  content: [
    "./*.html",
    "./_layouts/**/*.html",
    "./_includes/**/*.html",
    "./_posts/**/*.md"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#17211d",
        moss: "#51685d",
        fern: "#6f8f3d",
        clay: "#b66f4a",
        paper: "#faf7f0",
        pearl: "#f2eee4"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Fraunces", "Georgia", "serif"]
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
