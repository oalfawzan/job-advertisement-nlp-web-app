# Job Advertisement NLP Web App

This repository contains the implementation of a web-based job advertisement application that utilizes Natural Language Processing (NLP) techniques to classify and manage job listings.

## Overview

- **Author**: Osama Alfawzan
- **Date**: 2022-10-02
  
The project consists of two main milestones:

1. **Natural Language Processing (Milestone I)**: In this phase, we preprocess a collection of job advertisement documents, build machine learning models for document classification, and evaluate the models.
2. **Web-based Data Application (Milestone II)**: Here, we develop a job hunting website using the Flask framework. The website allows users to browse existing job advertisements and for employers to create new job listings. The site also integrates the NLP models from Milestone I to auto-classify job categories.

## Features

- **Job Preprocessing and Classification:** The code utilizes NLP techniques to preprocess job descriptions and classify them into relevant categories.
- **Job Display:** The Flask app allows the user to view available job advertisements.
- **Create a New Job Listing:** The user can create new job listings, and the system will recommend categories based on the provided description.

## Running the Code

### 1. For Milestone I tasks:

- Execute the Jupyter notebooks:
- - `milstone-1-task-1.ipynb`
- - `milstone-1-task-2-3.ipynb`

### 2. For Milestone II (Flask Web App):

- Navigate to the `job-ads` directory: ```cd job-ads```
- Run the Flask application: ```python app.py```
- Open a web browser and navigate to ```http://127.0.0.1:5000/``` to access the website.

## Acknowledgements

- RMIT University for the project guidelines and dataset.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
