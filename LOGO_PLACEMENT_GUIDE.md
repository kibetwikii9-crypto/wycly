# 🎨 Logo Placement Guide for Automify AI

## Logo Files Required

Please place the following logo files in the `frontend/public/` directory:

1. **`logo-main.svg`** - Main logo (with tagline "Create. Grow. Multiply.")
   - Used in: Sidebar, Login page
   - Format: SVG (preferred) or PNG
   - Recommended size: 200px width minimum

2. **`logo-main-no-tagline.svg`** - Main logo without tagline
   - Used in: Compact spaces, favicon
   - Format: SVG (preferred) or PNG
   - Recommended size: 200px width minimum

3. **`logo-white.svg`** - White version with tagline
   - Used in: Dark mode backgrounds
   - Format: SVG (preferred) or PNG
   - Recommended size: 200px width minimum

4. **`logo-white-no-tagline.svg`** - White version without tagline
   - Used in: Dark mode compact spaces
   - Format: SVG (preferred) or PNG
   - Recommended size: 200px width minimum

5. **`favicon.ico`** - Favicon for browser tabs
   - Format: ICO or PNG
   - Recommended size: 32x32px or 64x64px

## Current Logo Usage

### Sidebar (`frontend/components/Sidebar.tsx`)
- Uses: `logo-main.svg`
- Location: Top of sidebar
- Fallback: Text "Automify AI" if logo not found

### Login Page (`frontend/app/login/page.tsx`)
- Uses: `logo-main.svg`
- Location: Above login form
- Size: h-12 (48px height)

### Future Logo Placements (To Be Implemented)
- Header component
- Email templates
- PDF exports
- Mobile app icon

## Logo Specifications

Based on your brand guidelines:
- **Primary Color**: #007fff (blue)
- **Secondary Color**: Black (#000000)
- **Text Color**: Dark gray (almost black)
- **White Version**: For dark backgrounds

## Notes

- All logos should maintain aspect ratio
- SVG format is preferred for scalability
- Ensure logos are optimized for web (compressed)
- Test logos in both light and dark modes

