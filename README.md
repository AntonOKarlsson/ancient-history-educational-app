# SagaAHA - Ancient History Web App

An educational web application for ancient history students covering Pre-Greek civilizations through the end of the Middle Ages. All content in Icelandic.

## Random Greek Quiz Feature

The application now includes a random Greek quiz feature that presents 5 randomly selected questions about Ancient Greek history. This feature allows users to test their knowledge in a quick and engaging way.

### Features
- Randomly selects 5 questions from a pool of 60 Greek history questions
- Multiple-choice questions with immediate feedback
- Score tracking and results display
- Works for both authenticated and anonymous users (but only authenticated users' scores are saved)

### How to Use
1. Navigate to the Quiz section of the application
2. Click on the "Random Greek Quiz" featured quiz
3. Answer the 5 questions presented
4. Submit your answers to see your score and feedback

### Technical Details
- The questions are stored in the database and can be populated using the `populate_greek_quiz` management command
- The quiz uses the existing quiz models and views with a specialized view for random selection
- The feature is accessible at `/quiz/random-greek/`

## How to Run the Application

### Prerequisites
- Python 3.8 or higher
- Django 5.2 or higher

### Steps to Run the Application

1. **Clone or download the repository**

2. **Navigate to the project directory**
   ```
   cd path\to\SagaAHA
   ```

3. **Install required dependencies**
   ```
   pip install -r requirements.txt
   ```
   If requirements.txt is not available, install Django:
   ```
   pip install django
   ```

4. **Run database migrations**
   ```
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

6. **Start the development server**
   ```
   python manage.py runserver
   ```

7. **Access the application in your web browser**
   - Open your web browser and go to: http://localhost:8000/
   - For the admin interface: http://localhost:8000/admin/

## Project Structure

The application is divided into four main modules:

1. **Core** - Basic functionality, user profiles, and shared models
2. **Timeline** - Interactive historical timeline with events
3. **Reference** - Encyclopedia-like reference for historical figures, deities, etc.
4. **Quiz** - Educational quizzes and tests

## Features

- Interactive timeline with major historical events
- Comprehensive reference sections for historical figures, deities, governments, etc.
- Educational quizzes with various question types
- Progress tracking for users
- All content available in Icelandic

## Development

To create template directories for each app:
```
mkdir templates\core templates\timeline templates\reference templates\quiz
```

To create static files directories:
```
mkdir static\css static\js static\images
```
