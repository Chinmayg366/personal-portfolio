export const portfolioData = {
  name: "Chinmay Gurav",
  role: "Full-Stack Engineer",
  tagline: "I build fast, accessible, and well-crafted web products.",
  location: "India",
  email: "chinmay@example.com",
  social: {
    github: "https://github.com/Chinmayg366",
    linkedin: "https://www.linkedin.com/in/chinmay-gurav-55a38426a/",
    twitter: "https://twitter.com/",
  },
  about: [
    "I'm a full-stack engineer focused on building thoughtful interfaces and reliable systems. I enjoy turning ambiguous problems into clean, shippable products.",
    "Currently exploring the intersection of design systems, performance, and developer experience. Outside of code, I read, travel, and tinker with side projects.",
  ],
  stats: [
    { label: "Years coding", value: "4+" },
    { label: "Projects shipped", value: "20+" },
    { label: "Open-source PRs", value: "30+" },
  ],
  skills: {
    Languages: ["TypeScript", "JavaScript", "Python", "Java", "SQL"],
    Frontend: ["React", "Next.js", "Tailwind CSS", "Framer Motion", "Vite"],
    Backend: ["Node.js", "Express", "FastAPI", "PostgreSQL", "MongoDB"],
    Tooling: ["Git", "Docker", "AWS", "Vercel", "GitHub Actions"],
  } as Record<string, string[]>,
  projects: [
    {
      title: "Realtime Collab Editor",
      description:
        "A multiplayer text editor with CRDT-based syncing, presence cursors, and offline-first persistence.",
      tags: ["React", "Yjs", "WebSockets", "Postgres"],
      live: "#",
      code: "#",
      year: "2025",
    },
    {
      title: "Devboard Analytics",
      description:
        "An open-source dashboard that visualizes GitHub contribution velocity across teams and repos.",
      tags: ["Next.js", "TypeScript", "tRPC", "Prisma"],
      live: "#",
      code: "#",
      year: "2024",
    },
    {
      title: "Lumen UI Kit",
      description:
        "A minimal, accessible component library built on Radix primitives with a strict design-token system.",
      tags: ["React", "Radix UI", "Tailwind", "Storybook"],
      live: "#",
      code: "#",
      year: "2024",
    },
    {
      title: "Pathfinder Visualizer",
      description:
        "Interactive visualization of pathfinding algorithms (A*, Dijkstra, BFS) with maze generators.",
      tags: ["React", "Canvas", "Algorithms"],
      live: "#",
      code: "#",
      year: "2023",
    },
  ],
  experience: [
    {
      role: "Software Engineer",
      company: "Freelance",
      period: "2023 — Present",
      description:
        "Designing and shipping web apps for early-stage startups: marketing sites, dashboards, and internal tools.",
    },
    {
      role: "Engineering Intern",
      company: "Tech Startup",
      period: "2022 — 2023",
      description:
        "Built features across the React frontend and Node backend; improved page load by 40% via code-splitting and image optimization.",
    },
  ],
};

export type PortfolioData = typeof portfolioData;
