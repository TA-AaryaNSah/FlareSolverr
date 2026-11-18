FROM ghcr.io/flaresolverr/flaresolverr:latest

# Render dynamically binds the port to $PORT environment variable
ENV PORT=8191
EXPOSE 8191
