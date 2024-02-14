python -m venv venv
. venv/bin/activate

# Run pip install only if  PREBUILT is either not set or an empty string
if [ -z "$PREBUILT" ]; then
  pip install -r requirements.txt
fi

# The script creates a disasters.nt file
python -u main.py

LC_ALL=C sort -u -o disasters.sorted.nt disasters.nt
lbzip2 disasters.sorted.nt
mv disasters.sorted.nt.bz2 disasters.nt.bz2

