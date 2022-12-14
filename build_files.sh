echo "Build Start"
python -m pip install -r requirnments.txt
python manage.py collectstatic --noinput --clear
echo "Build END"