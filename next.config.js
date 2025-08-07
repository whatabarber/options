/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    PYTHON_API_URL: process.env.PYTHON_API_URL || 'http://localhost:5000',
  },
  async rewrites() {
    return [
      {
        source: '/python-api/:path*',
        destination: `${process.env.PYTHON_API_URL || 'http://localhost:5000'}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;