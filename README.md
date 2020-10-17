# GTDSL-GCalendar

## Introduction

A wrapper around Google calendar API with the focus of providing Getting Things Done friendly setup.
This project is currently a module of [GTDSL-Notion](https://github.com/Yeboster/GTDSL-Notion) (A Notion implementation of GTD).

## Features
- CRUD:
  - Create a google calendar event;
  - Create time repetition events (~~1 hour~~, 1 day, 1 week, 1 month);
  - Find already existing events by title;
  - Delete event by title.

## Technologies
The project is Python 3.8 and [Pipenv](https://pipenv.pypa.io/en/latest/) as dependency manager.

In the near future it will be packed also as a micro-service (Docker & API support using Flask).

## Getting Started
- Clone the repository;
- Setup dependencies with Pipenv by running: `pipenv install`
- Build the pip package by running 
  ```shell
  chmod +x setup.py && ./setup.py install
  ```

## Contributing

Contributions are welcome ❤️

If you'd like to improve this project checkout the [Contributing guide](CONTRIBUTING.md).