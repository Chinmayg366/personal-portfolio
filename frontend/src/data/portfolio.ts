export const portfolioData = {
  name: "Chinmay Gurav",
  role: "Aspiring Data Analyst",
  tagline:
    "Computer Applications graduate building efficient, scalable software with a focus on data-driven insights.",
  location: "Navi Mumbai, India",
  email: "tech.chinmayg@gmail.com",
  phone: "+91 7738724169",
  address: "B-15, Channel Residency, Takka Road, Panvel, Navi Mumbai, India",
  resumeUrl: "/resume.pdf",
  social: {
    github: "https://github.com/Chinmayg366",
    linkedin: "https://www.linkedin.com/in/chinmay-gurav-55a38426a/",
    twitter: "https://twitter.com/",
  },
  about: [
    "I'm a Computer Applications graduate with a strong foundation in Java, Python, and web development. I'm passionate about building efficient and scalable software solutions.",
    "Currently pursuing my MCA at Amity University to deepen my technical expertise. I'm eager to grow as a developer in a collaborative environment, with a focus on data analysis and technology-driven insights.",
  ],
  stats: [
    { label: "Languages spoken", value: "4" },
    { label: "Years learning", value: "5+" },
    { label: "Degree in progress", value: "MCA" },
  ],
  skills: {
    Languages: ["Java", "Python", "C", "C++", "JavaScript"],
    "Web Development": ["HTML", "CSS", "JavaScript", "ReactJS"],
    "Tools & Tech": ["DSA", "Optimization Techniques", "Digital Marketing"],
    "Soft Skills": [
      "Time Management",
      "Team Player",
      "Problem Solving",
      "Collaboration",
      "Communication",
    ],
    Languages_Spoken: ["English", "Hindi", "Marathi", "Spanish"],
  } as Record<string, string[]>,
  projects: [
    {
      title: "Personal Portfolio",
      description:
        "A modern, terminal-inspired personal portfolio built with React, Vite and Tailwind CSS featuring light/dark mode.",
      tags: ["React", "TypeScript", "Tailwind CSS", "Vite"],
      live: "#",
      code: "https://github.com/Chinmayg366/personal-portfolio",
      year: "2025",
    },
    {
      title: "Java Practice Suite",
      description:
        "Collection of Java programs exploring OOP concepts, data structures, and algorithmic problem solving.",
      tags: ["Java", "DSA", "OOP"],
      live: "#",
      code: "https://github.com/Chinmayg366",
      year: "2024",
    },
    {
      title: "Python Data Explorations",
      description:
        "Notebooks and scripts for cleaning, analyzing and visualizing datasets — a stepping stone into data analytics.",
      tags: ["Python", "Pandas", "Data Analysis"],
      live: "#",
      code: "https://github.com/Chinmayg366",
      year: "2024",
    },
    {
      title: "ReactJS Mini Apps",
      description:
        "A series of small React applications built to practice components, state management, and modern web patterns.",
      tags: ["ReactJS", "JavaScript", "HTML", "CSS"],
      live: "#",
      code: "https://github.com/Chinmayg366",
      year: "2023",
    },
  ],
  experience: [
    {
      role: "Master of Computer Applications (MCA)",
      company: "Amity University",
      period: "2024 — 2026",
      description:
        "Pursuing MCA with a focus on advanced software development, data analysis, and modern technology stacks.",
    },
    {
      role: "Bachelor of Computer Applications (BCA)",
      company: "TMV University",
      period: "2020 — 2023",
      description:
        "Built foundations in programming, web development, databases, and computer science fundamentals.",
    },
  ],
};

export type PortfolioData = typeof portfolioData;
