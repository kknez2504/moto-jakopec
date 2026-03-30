/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "www.kawasaki.eu" },
      { protocol: "https", hostname: "www.dks.si" },
    ],
  },
};

export default nextConfig;
