#!/usr/bin/env python3
from os import system, popen
from common import echo

ignore_projects = ["lh_maps", "light_holes_12states"]

# Current directory
PWD = popen("echo $PWD").read().split("/")[-1].rstrip("\n")


# Remove file of given path and filename
def remove(path, file):
    system("rm " + path + file)


def read_list_from_ls(path):
    return popen("ls {}".format(path)).read().split()


# Clear unnecessary files
def clear_files(projectname=''):
    # Intro message
    echo("Removing unnecessary files started")

    if projectname:
        projects = [projectname]
    else:
        # Get list of the projects
        projects = read_list_from_ls("~/Storage/{}/results/".format(PWD))

    # Loop over all projects
    for project in projects:
        if project in ignore_projects:
            continue
        echo("Removing unnecessary files in {}".format(project))
        # Path to WaveFuns of a given project
        path = "~/Storage/{}/results/{}/WaveFuns/".format(PWD, project)
        # Get list of all files in the WaveFuns directory
        files = read_list_from_ls(path)

        # Temporary variables
        current_n_str, last_bin_file = 0, ""

        # Loop over all files
        for file in files:
            # Remove any maps, gnuplot files and info files
            if "map" in file or "spec.plt" in file or "info" in file:
                remove(path, file)

            # Remove bin_h if not the most recent
            # elif is necessary as "info" file contains "bin_h" substring
            elif "bin_h" in file:
                # Remove bin_h if n_str repeats
                # Files should be sorted by n_str by ls
                n_str = int(file[1:5])
                if n_str == current_n_str:
                    remove(path, last_bin_file)

                # Update last bin data
                current_n_str = n_str
                last_bin_file = file

    # Outro message
    echo("Unnecessary files cleared")


# Run the script
if __name__ == "__main__":
    clear_files()
