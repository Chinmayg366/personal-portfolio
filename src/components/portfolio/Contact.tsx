import { ArrowUpRight, Github, Linkedin, Mail } from "lucide-react";
import { portfolioData } from "@/data/portfolio";

const Contact = () => {
  const { email, social } = portfolioData;
  return (
    <section id="contact" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-6xl mx-auto px-6">
        <div className="reveal max-w-3xl">
          <div className="mono-label mb-3">// 04 — contact</div>
          <h2 className="text-4xl md:text-6xl font-semibold tracking-tight leading-[1.05]">
            Let's build <br />
            <span className="text-muted-foreground">something good together.</span>
          </h2>
          <p className="mt-6 text-lg text-muted-foreground max-w-xl">
            Open to freelance projects, full-time roles, and interesting collaborations. The fastest
            way to reach me is over email.
          </p>

          <a
            href={`mailto:${email}`}
            className="group mt-8 inline-flex items-center gap-2 text-2xl md:text-3xl font-medium link-underline"
          >
            {email}
            <ArrowUpRight className="h-6 w-6 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
          </a>

          <div className="mt-10 flex items-center gap-3">
            <a
              href={social.github}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 h-10 px-4 rounded-md border border-border text-sm hover:bg-accent transition-colors"
            >
              <Github className="h-4 w-4" /> GitHub
            </a>
            <a
              href={social.linkedin}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 h-10 px-4 rounded-md border border-border text-sm hover:bg-accent transition-colors"
            >
              <Linkedin className="h-4 w-4" /> LinkedIn
            </a>
            <a
              href={`mailto:${email}`}
              className="inline-flex items-center gap-2 h-10 px-4 rounded-md border border-border text-sm hover:bg-accent transition-colors"
            >
              <Mail className="h-4 w-4" /> Email
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
