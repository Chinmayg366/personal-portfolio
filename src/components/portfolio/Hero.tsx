import { ArrowDown, Github, Linkedin, Mail } from "lucide-react";
import { portfolioData } from "@/data/portfolio";

const Hero = () => {
  const { name, role, tagline, social, email } = portfolioData;

  return (
    <section id="top" className="relative min-h-screen flex items-center pt-24 pb-20 overflow-hidden">
      <div className="absolute inset-0 bg-grid pointer-events-none" aria-hidden="true" />

      <div className="relative max-w-6xl mx-auto px-6 w-full">
        <div className="mono-label mb-6">// portfolio — v1.0</div>

        <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[0.95]">
          {name.split(" ")[0]}
          <br />
          <span className="text-muted-foreground">{name.split(" ").slice(1).join(" ")}.</span>
        </h1>

        <div className="mt-8 max-w-2xl">
          <p className="mono text-sm text-muted-foreground">
            <span className="text-foreground">~$</span> whoami<span className="caret" />
          </p>
          <p className="mt-3 text-xl md:text-2xl text-foreground">
            {role}. {tagline}
          </p>
        </div>

        <div className="mt-10 flex flex-wrap items-center gap-3">
          <a
            href="#projects"
            className="inline-flex h-11 items-center gap-2 rounded-md bg-foreground text-background px-5 text-sm font-medium hover:opacity-90 transition-opacity"
          >
            View work
            <ArrowDown className="h-4 w-4" />
          </a>
          <a
            href="#contact"
            className="inline-flex h-11 items-center rounded-md border border-border px-5 text-sm font-medium hover:bg-accent transition-colors"
          >
            Get in touch
          </a>

          <div className="flex items-center gap-1 ml-2">
            <a
              href={social.github}
              target="_blank"
              rel="noreferrer"
              aria-label="GitHub"
              className="h-10 w-10 inline-flex items-center justify-center rounded-md hover:bg-accent transition-colors"
            >
              <Github className="h-4 w-4" />
            </a>
            <a
              href={social.linkedin}
              target="_blank"
              rel="noreferrer"
              aria-label="LinkedIn"
              className="h-10 w-10 inline-flex items-center justify-center rounded-md hover:bg-accent transition-colors"
            >
              <Linkedin className="h-4 w-4" />
            </a>
            <a
              href={`mailto:${email}`}
              aria-label="Email"
              className="h-10 w-10 inline-flex items-center justify-center rounded-md hover:bg-accent transition-colors"
            >
              <Mail className="h-4 w-4" />
            </a>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-3 gap-6 max-w-md">
          {portfolioData.stats.map((s) => (
            <div key={s.label}>
              <div className="text-3xl font-semibold">{s.value}</div>
              <div className="mono-label mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Hero;
