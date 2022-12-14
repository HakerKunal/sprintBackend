echo "Build Start"
python3.9 -m pip install -r requirnments.txt
python 3.9 manage.py collectstatic --noinput --clear
echo "Build END"