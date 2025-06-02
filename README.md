# Ancient History Educational App (Fornaldarsögu-app)

An interactive educational web application for learning ancient history from pre-Greek civilizations through the Middle Ages, designed specifically for Icelandic students.

## Features
- Interactive timeline of historical events
- Comprehensive who's who database
- Multiple choice quizzes for each period
- Gods and deities glossary
- Responsive design for desktop and mobile

## Historical Periods Covered
- Pre-Greek Civilizations (Fyrir-grísk siðmenning)
- Ancient Greece (Grikkland)
- Roman Empire (Rómaveldi)
- Middle Ages (Miðaldir)

## Technologies Used
- HTML5, CSS3, JavaScript
- Responsive design
- Local storage for progress tracking

## Getting Started
1. Clone this repository
2. Open `index.html` in your web browser
3. Start exploring ancient history!

## Language
This application is designed for Icelandic students and all content is in Icelandic.

## Deployment and Data Population
When deploying to Heroku or updating content, make sure to run the appropriate management commands to populate the database.

### Automatic Population on Heroku
For automatic population on Heroku deployment, rename `Procfile.release` to `Procfile` or add its contents to your existing `Procfile`:

```
release: bash scripts/release.sh
web: gunicorn SagaAHA.wsgi
```

This will automatically run the release script whenever you deploy to Heroku.

### Using the Release Script
The easiest way to populate the database is to use the provided release script:

#### On Linux/Mac:
```bash
# Run this script on your local machine
bash scripts/release.sh

# Run this script on Heroku
heroku run bash scripts/release.sh --app your-app-name
```

#### On Windows:
```cmd
# Run this script on your local machine
scripts\release.bat

# For Heroku, use the bash script with Git Bash or WSL
```

### Manual Population
Alternatively, you can run each command individually:

```bash
# Run these commands on your local machine to populate the database
python manage.py populate_periods
python manage.py populate_greek_content
python manage.py populate_roman_content
python manage.py populate_middle_ages_content
```

For Heroku deployment, run these commands using the Heroku CLI:

```bash
# Run these commands after deploying to Heroku
heroku run python manage.py populate_periods --app your-app-name
heroku run python manage.py populate_greek_content --app your-app-name
heroku run python manage.py populate_roman_content --app your-app-name
heroku run python manage.py populate_middle_ages_content --app your-app-name
```

Replace `your-app-name` with your actual Heroku app name.

### Troubleshooting
If content is not showing up on the site after deployment, it's likely that the database population commands have not been run. Run the release script or the individual commands to populate the database.

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
MIT License
