import { ArrowUpRight, Github } from "lucide-react";
import { portfolioData } from "@/data/portfolio";

const Projects = () => {
  return (
    <section id="projects" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex items-end justify-between mb-12 reveal">
          <div>
            <div className="mono-label mb-3">// 03 — selected work</div>
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
              Things I've built.
            </h2>
          </div>
          <a
            href={portfolioData.social.github}
            target="_blank"
            rel="noreferrer"
            className="hidden sm:inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground link-underline"
          >
            All projects on GitHub <ArrowUpRight className="h-4 w-4" />
          </a>
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          {portfolioData.projects.map((p) => (
            <article
              key={p.title}
              className="group relative rounded-lg border border-border bg-card p-6 hover:border-foreground/30 transition-colors reveal"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="mono text-xs text-muted-foreground mb-2">{p.year}</div>
                  <h3 className="text-xl font-semibold tracking-tight">{p.title}</h3>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  <a
                    href={p.code}
                    target="_blank"
                    rel="noreferrer"
                    aria-label={`${p.title} source`}
                    className="h-8 w-8 inline-flex items-center justify-center rounded-md hover:bg-accent transition-colors"
                  >
                    <Github className="h-4 w-4" />
                  </a>
                  <a
                    href={p.live}
                    target="_blank"
                    rel="noreferrer"
                    aria-label={`${p.title} live`}
                    className="h-8 w-8 inline-flex items-center justify-center rounded-md hover:bg-accent transition-colors"
                  >
                    <ArrowUpRight className="h-4 w-4" />
                  </a>
                </div>
              </div>

              <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
                {p.description}
              </p>

              <div className="mt-5 flex flex-wrap gap-1.5">
                {p.tags.map((t) => (
                  <span
                    key={t}
                    className="mono text-[11px] px-2 py-1 rounded border border-border text-muted-foreground"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Projects;
