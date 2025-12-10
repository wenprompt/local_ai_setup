#!/usr/bin/env python3
"""
start_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Project name is defined in docker-compose.yml as "localai".
"""

import os
import subprocess
import shutil
import argparse


def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "https://github.com/supabase/supabase.git",
            ]
        )
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")


def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)


def stop_existing_containers(profile=None):
    print("Stopping and removing existing containers...")
    cmd = ["docker", "compose"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "down"])
    run_command(cmd)


def start_services(profile=None):
    """Start all services (Supabase + local AI) using the main compose file."""
    print("Starting all services...")
    cmd = ["docker", "compose", "-f", "docker-compose.yml"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["up", "-d"])
    run_command(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Start the local AI and Supabase services."
    )
    parser.add_argument(
        "--profile",
        choices=["cpu", "gpu-nvidia", "gpu-amd", "none"],
        default="cpu",
        help="Profile to use for Docker Compose (default: cpu)",
    )
    args = parser.parse_args()

    clone_supabase_repo()
    prepare_supabase_env()

    stop_existing_containers(args.profile)

    # Start all services (Supabase is included in docker-compose.yml)
    start_services(args.profile)


if __name__ == "__main__":
    main()

## RUN ##
# python start_services.py --profile gpu-nvidia

## To Upgrade containers
# # Stop all services
# docker compose -f docker-compose.yml --profile gpu-nvidia down

# # Pull latest versions of all containers
# docker compose -f docker-compose.yml --profile gpu-nvidia pull

# # Start services again with your desired profile
# python start_services.py --profile gpu-nvidia
