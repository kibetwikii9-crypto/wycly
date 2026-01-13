/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // No rewrites needed - axios handles API URLs via NEXT_PUBLIC_API_URL
  images: {
    // Ensure images are optimized and not cached too aggressively
    unoptimized: false,
    // Add cache headers for static assets
    minimumCacheTTL: 60,
  },
  // Add headers to prevent aggressive caching of logo files
  async headers() {
    return [
      {
        source: '/:path*.png',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, must-revalidate',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;



