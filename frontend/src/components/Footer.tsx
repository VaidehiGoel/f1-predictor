function Footer() {
  return (
    <footer className="border-t border-white/5 mt-20">
      <div className="max-w-6xl mx-auto px-6 py-8 flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
          <span className="w-1 h-4 bg-race-red skew-x-[-12deg]" />
          <span className="font-display font-bold">
            GRID<span className="text-race-red">CAST</span>
          </span>
        </div>

        <p className="text-muted text-xs">
          Built with FastF1, XGBoost, and React · Not affiliated with Formula 1
        </p>

        <div className="flex gap-4 font-mono text-xs text-muted">
            <a
            href="https://github.com/VaidehiGoel/f1-predictor.git"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-ink transition-colors"
          >
            GitHub @Vaidehi Goel
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;