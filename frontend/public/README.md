# 📁 Public Assets Directory

This directory contains static assets that are served at the root URL path.

## Logo Files - Place Directly Here

Place these files **directly in this folder** (not in a subfolder):

```
frontend/public/
├── logo-main.svg                    ← Place here
├── logo-main-no-tagline.svg        ← Place here
├── logo-white.svg                  ← Place here
├── logo-white-no-tagline.svg       ← Place here
└── favicon.ico                     ← Place here
```

## How Next.js Serves These Files

Files in `frontend/public/` are accessible at the root path `/`:

- `frontend/public/logo-main.svg` → Accessible at `/logo-main.svg`
- `frontend/public/favicon.ico` → Accessible at `/favicon.ico`

## Required Files

1. **logo-main.svg** - Main logo with tagline (used in sidebar and login)
2. **logo-white.svg** - White version with tagline (for dark mode)
3. **logo-main-no-tagline.svg** - Logo without tagline (optional, for compact spaces)
4. **logo-white-no-tagline.svg** - White logo without tagline (optional)
5. **favicon.ico** - Browser tab icon (32x32 or 64x64 pixels)

## File Format Notes

- **SVG** is preferred (scalable, smaller file size)
- **PNG** is also acceptable (use `.png` extension instead of `.svg`)
- Files should be optimized for web use

## Current Usage

- Sidebar: Uses `/logo-main.svg` (light mode) and `/logo-white.svg` (dark mode)
- Login Page: Uses `/logo-main.svg` (light mode) and `/logo-white.svg` (dark mode)
- Favicon: Uses `/favicon.ico` in browser tab

