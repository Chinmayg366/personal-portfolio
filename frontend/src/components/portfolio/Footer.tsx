import { portfolioData } from "@/data/portfolio";

const Footer = () => {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-border py-10">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <p className="mono text-xs text-muted-foreground">
          © {year} {portfolioData.name}. Crafted with care.
        </p>
        <p className="mono text-xs text-muted-foreground">
          <span className="text-foreground">~$</span> echo "thanks for visiting"
        </p>
      </div>
    </footer>
  );
};

export default Footer;
