// E-mail through Resend (resend.com). RESEND_API_URL can point elsewhere for tests. All mail is HTML with a plain-text
// twin, in the site's look: the logo on top, white card on the light grey, blue buttons, the company's details below.
import { config, env, optionalEnv } from "./env.ts";

// The site's colours (the theme in content/baseline.json).
const C = { ink: "#121418", text: "#3B4048", muted: "#646B75", line: "#E3E7EC", bg: "#F1F3F6", blue: "#1572D3", danger: "#B42318" };
const FONT = "'Plus Jakarta Sans',Helvetica,Arial,sans-serif";

export interface Mail {
  to: string | string[];
  subject: string;
  /** Paragraphs and other blocks, see block helpers below. */
  blocks: string[];
  replyTo?: string;
}

const escapeHtml = (text: string) =>
  text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");

export const block = {
  heading: (text: string) =>
    `<h1 style="margin:0 0 18px;font-family:${FONT};font-size:24px;line-height:1.25;font-weight:700;letter-spacing:-0.02em;color:${C.ink}">${escapeHtml(text)}</h1>`,
  text: (text: string) => `<p style="margin:0 0 14px;font-size:16px;line-height:1.6;color:${C.text}">${escapeHtml(text)}</p>`,
  rows: (rows: [string, string][]) =>
    `<table role="presentation" style="width:100%;border-collapse:collapse;margin:0 0 22px">${rows
      .map(
        ([label, value]) =>
          `<tr><td style="padding:11px 16px 11px 0;border-bottom:1px solid ${C.line};font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:${C.muted};white-space:nowrap;vertical-align:top">${escapeHtml(label)}</td><td style="padding:10px 0;border-bottom:1px solid ${C.line};font-size:15px;line-height:1.5;color:${C.ink}">${escapeHtml(value).replace(/\n/g, "<br>")}</td></tr>`
      )
      .join("")}</table>`,
  button: (label: string, href: string, tone: "primary" | "danger" = "primary") =>
    `<p style="margin:8px 0 6px"><a href="${escapeHtml(href)}" style="display:inline-block;padding:14px 28px;border-radius:999px;background:${
      tone === "danger" ? C.danger : C.blue
    };color:#ffffff;font-family:${FONT};font-weight:700;font-size:15px;text-decoration:none">${escapeHtml(label)} &rarr;</a></p>`,
  small: (text: string) => `<p style="margin:18px 0 0;font-size:13px;line-height:1.5;color:${C.muted}">${escapeHtml(text)}</p>`,
};

function html(mail: Mail): string {
  const site = config.siteUrl().replace(/\/$/, "");
  return `<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"></head>
<body style="margin:0;padding:0;background:${C.bg};font-family:${FONT};-webkit-text-size-adjust:100%">
<table role="presentation" width="100%" style="width:100%;border-collapse:collapse;background:${C.bg}"><tr><td style="padding:28px 14px">
<table role="presentation" width="100%" style="max-width:580px;margin:0 auto;border-collapse:collapse">
<tr><td style="padding:0 4px 18px"><a href="${escapeHtml(site)}/" style="text-decoration:none"><img src="${escapeHtml(site)}/logo-mork.png" width="150" height="53" alt="Västkust Bygg &amp; Montage AB" style="display:block;border:0;width:150px;height:auto"></a></td></tr>
<tr><td style="background:#ffffff;border-radius:12px;border-top:4px solid ${C.blue};padding:32px 30px 30px">${mail.blocks.join("")}</td></tr>
<tr><td style="padding:20px 4px 0;font-size:12.5px;line-height:1.6;color:${C.muted}">Västkust Bygg &amp; Montage AB &middot; 076-882 03 33 &middot; <a href="mailto:info@vastkustbygg.se" style="color:${C.muted}">info@vastkustbygg.se</a><br>Org.nr 559071-1999 &middot; <a href="${escapeHtml(site)}/" style="color:${C.muted}">${escapeHtml(site.replace(/^https?:\/\//, ""))}</a></td></tr>
</table></td></tr></table></body></html>`;
}

function plain(mail: Mail): string {
  return mail.blocks
    .map((b) =>
      b
        .replace(/ &rarr;/g, "")
        .replace(/<br>/g, "\n")
        .replace(/<a [^>]*href="([^"]+)"[^>]*>([^<]*)<\/a>/g, "$2: $1")
        .replace(/<\/(p|h1|tr)>/g, "\n")
        .replace(/<\/td><td[^>]*>/g, ": ")
        .replace(/<[^>]+>/g, "")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
    )
    .join("\n")
    .trim();
}

/** Sends one e-mail; returns false (and logs) instead of throwing, so a mail problem never undoes the action itself. */
export async function sendMail(mail: Mail): Promise<boolean> {
  const apiKey = optionalEnv("RESEND_API_KEY");
  if (!apiKey) {
    console.error("RESEND_API_KEY is not set; e-mail not sent:", mail.subject);
    return false;
  }
  try {
    const response = await fetch(`${env("RESEND_API_URL", "https://api.resend.com")}/emails`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: env("EMAIL_FROM", "Västkust Bygg <onboarding@resend.dev>"),
        to: Array.isArray(mail.to) ? mail.to : [mail.to],
        subject: mail.subject,
        html: html(mail),
        text: plain(mail),
        ...(mail.replyTo ? { reply_to: mail.replyTo } : {}),
      }),
    });
    if (!response.ok) {
      console.error("Resend refused the e-mail:", response.status, await response.text());
      return false;
    }
    return true;
  } catch (error) {
    console.error("Could not reach Resend:", error);
    return false;
  }
}
