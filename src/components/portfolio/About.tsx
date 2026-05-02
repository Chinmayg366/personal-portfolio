import { portfolioData } from "@/data/portfolio";

const About = () => {
  return (
    <section id="about" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid md:grid-cols-12 gap-10">
          <div className="md:col-span-4 reveal">
            <div className="mono-label mb-3">// 01 — about</div>
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
              A bit about me.
            </h2>
          </div>
          <div className="md:col-span-8 space-y-4 reveal">
            {portfolioData.about.map((p, i) => (
              <p key={i} className="text-base md:text-lg text-muted-foreground leading-relaxed">
                {p}
              </p>
            ))}

            <div className="pt-6 mt-6 border-t border-border">
              <div className="mono-label mb-4">// experience</div>
              <ul className="space-y-6">
                {portfolioData.experience.map((e) => (
                  <li key={e.role + e.company} className="grid sm:grid-cols-3 gap-2">
                    <div className="mono text-xs text-muted-foreground">{e.period}</div>
                    <div className="sm:col-span-2">
                      <div className="font-medium">
                        {e.role} <span className="text-muted-foreground">· {e.company}</span>
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">{e.description}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
