# Super Heroes API

A Flask-based REST API for managing superheroes, their powers, and relationships between them.

**Owner:** Brian Muigai

## Description

This application provides a comprehensive API for superhero management, allowing users to create, read, update, and manage heroes, their superpowers, and the relationships between them. Built with Flask and SQLAlchemy for robust data management.

## Features

- **Hero Management**: Create and retrieve superhero profiles
- **Power Management**: Manage superpowers with validation
- **Hero-Power Relationships**: Associate heroes with powers and strength levels
- **RESTful API**: Clean, intuitive endpoints
- **Data Validation**: Ensures data integrity
- **SQLite Database**: Lightweight, portable data storage

## Setup Instructions

### Prerequisites
- Python 3.8+
- pipenv

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd super-heroes
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Activate virtual environment:
   ```bash
   pipenv shell
   ```

4. Initialize database:
   ```bash
   cd server
   python seed.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`

## API Endpoints

- `GET /heroes` - List all heroes
- `GET /heroes/<id>` - Get specific hero with powers
- `GET /powers` - List all powers
- `GET /powers/<id>` - Get specific power
- `PATCH /powers/<id>` - Update power description
- `POST /hero_powers` - Create hero-power relationship

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite

## Support

For questions or issues, contact Brian Muigai.

## License

This project is licensed under the MIT License.