import { portfolioData } from "@/data/portfolio";

const Skills = () => {
  return (
    <section id="skills" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid md:grid-cols-12 gap-10">
          <div className="md:col-span-4 reveal">
            <div className="mono-label mb-3">// 02 — skills</div>
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
              Tools I work with.
            </h2>
            <p className="mt-4 text-muted-foreground">
              A working knowledge of the modern web stack — front to back.
            </p>
          </div>

          <div className="md:col-span-8 space-y-8 reveal">
            {Object.entries(portfolioData.skills).map(([group, items]) => (
              <div key={group}>
                <div className="flex items-baseline justify-between mb-3">
                  <h3 className="text-sm font-medium">{group}</h3>
                  <span className="mono text-xs text-muted-foreground">
                    {String(items.length).padStart(2, "0")}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {items.map((s) => (
                    <span
                      key={s}
                      className="mono text-xs px-3 py-1.5 rounded-md border border-border bg-secondary text-secondary-foreground hover:bg-accent transition-colors"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Skills;
