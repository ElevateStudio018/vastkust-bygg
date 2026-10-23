// The marks of the sites the reviews come from, shown on each review card: ServiceFinder's symbol (from the logo on
// servicefinder.se) and Google's G.
export function SourceLogo({ source }: { source: string }) {
  if (source === "servicefinder") {
    return (
      <svg viewBox="0 0 50 50" className="src-logo" aria-hidden="true">
        <path d="m18 5.6-18 18 5 5 18-18z" fill="#101F41" />
        <path d="m16 21.6c1.3 1.3 3.1 2.1 5 2.1s3.7-.8 5-2.1l6-6 13 13 5-5-18.1-18z" fill="#3960BF" />
        <path d="m28 23.6c-1.9 1.9-4.4 2.9-7 2.9s-5.1-1-7-2.9l-7 7 18.1 18 3-3-7-7 2-2 7 7 3-3-7-7 2-2 7 7 3-3-7-7 2-2 7 7 3-3.1-11.2-11z" fill="#101F41" />
      </svg>
    );
  }
  if (source === "google") {
    return (
      <svg viewBox="0 0 48 48" className="src-logo" aria-hidden="true">
        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
      </svg>
    );
  }
  return null;
}
