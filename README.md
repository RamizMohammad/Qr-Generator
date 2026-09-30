# Pillbox QR

A single-page QR code maker with pill-shaped modules, custom corner eyes, a center photo with brackets, gradients, presets, and a live scan check. Everything runs in the browser; nothing is uploaded anywhere.

## Project layout

```
index.html        the whole app (HTML, CSS, JS in one file)
favicon.svg       tab icon
vendor/           QR libraries, served from your own domain
vercel.json       Vercel settings: static hosting, clean URLs, security headers, caching
.vercelignore     files kept out of the deployment
```

## Deploy on Vercel

**From GitHub (recommended)**
1. Push this folder to GitHub (the `web` branch or `main`).
2. In Vercel, choose **Add New → Project** and import `RamizMohammad/Qr-Generator`.
3. Leave Framework Preset as **Other**. Leave Build Command and Output Directory empty; `vercel.json` already sets them.
4. Deploy. Every later push redeploys automatically. If you deploy from `web`, set it as the Production Branch under Project → Settings → Git.

**From the terminal**
```bash
npm i -g vercel
vercel          # preview deployment
vercel --prod   # production deployment
```

## Run locally

```bash
npx serve .
```
Then open the URL it prints. Open it through a server rather than double-clicking the file, so the `/vendor` scripts load.

## Notes

- The Content Security Policy in `vercel.json` only allows scripts from your own domain and fonts from Google Fonts. If you add analytics or another script host, add it to `script-src` and `connect-src`.
- Files in `/vendor` are cached for a year. If you replace one, give it a new file name so browsers fetch the new copy.

## Third-party code

- `vendor/qrcode.min.js`: [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator) 1.4.4 by Kazuhiko Arase, MIT License.
- `vendor/jsQR.min.js`: [jsQR](https://github.com/cozmo/jsQR) 1.4.0 by Cosmo Wolfe, Apache License 2.0.
