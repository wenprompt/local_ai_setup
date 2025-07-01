# Use the official n8n image as the base
FROM n8nio/n8n:latest

# Switch to root user to install packages (if necessary, then switch back)
# The n8n image might already be user 'node' with permissions.
# If direct npm install fails, you might need to manage users.
# For many n8n images, USER node is already set.
# Let's try installing in a way that works with the 'node' user or root.

# Option 1: Install globally (often works if Node.js path is configured)
# USER root # Switch to root if needed for global install permissions
# RUN npm install -g mammoth lodash
# USER node # Switch back to the default n8n user

# Option 2 (Often more reliable for n8n):
# Install packages into the n8n user's local node_modules or a specific path
# that n8n's Node.js runtime can access.
# The n8n user is 'node' and its home is /home/node.
# We can create a package.json and install there, or install directly.
# The documentation for NODE_FUNCTION_ALLOW_EXTERNAL implies n8n looks in its own main node_modules.
# This would usually be where n8n itself is installed, e.g., /usr/local/lib/node_modules/n8n
# Modifying this directly can be tricky.
# A common practice for extending n8n is to install packages in the user's .n8n folder,
# but for NODE_FUNCTION_ALLOW_EXTERNAL, it specifies n8n's *main* node_modules.

# Let's try a straightforward approach that often works for adding packages to n8n image:
# n8n's base image has npm. We can try to install into the main installation.
# The working directory for n8n is usually /data, but n8n itself is elsewhere.
#
# A robust way for the n8nio/n8n image:
# The image already has an n8n installation. The goal is to add modules
# where the existing Node.js (running n8n) can find them.
# Typically, n8n is installed in a way that its own dependencies are resolved.
# Adding to the main package.json of n8n and rebuilding is complex.
#
# A simpler approach for the n8nio/n8n Docker image is often to create a local package.json
# in the n8n user's home directory, install packages there, and set NODE_PATH.
# However, given the constraint "sourced from n8n/node_modules directory", let's assume
# we need to get it into a path Node.js will check by default or where n8n itself loads modules.
#
# Easiest method that usually works for n8nio/n8n image, ensuring modules are findable by n8n:
USER root
RUN npm install -g mammoth lodash
USER node