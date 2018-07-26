Building CDASH container via Singularity
=========================================

1. Login as root and copy all the files to `/root`

Next run `singularity build /tmp/CDASH.simg CDASH`

Once the container is built run `singularity instance.start /tmp/CDASH.simg cdash`

Go to your browser at `http://<localhost>/CDash/public` to view the Dashboards

