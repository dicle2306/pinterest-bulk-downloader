# Pinterest Bulk Downloader (ENG)

Welcome to the Pinterest Bulk Downloader! This tool is designed to automate the downloading of images from Pinterest boards efficiently.

## Requirements

- Python 3.x
- Selenium
- Requests library
- WebDriver (e.g., ChromeDriver)

## Installation

1. Ensure Python is installed on your system.
2. Install necessary Python libraries:

- pip install selenium requests webdriver-manager
  or
- pip install -r requirements.txt

3. Download the appropriate WebDriver for your browser and ensure it's accessible in your PATH.

## Configuration

Before running the script, please configure the following settings in the script:

- **Email**: Your Pinterest email address.
- **Password**: Your Pinterest password.
- **Sleep Time**: Adjust this delay to accommodate slow internet connections or computers. Increase the time if you're experiencing incomplete page loads.
- **URL**: The URL of the Pinterest board you want to download images from.
- **Folder Structure**: When enabled, images are organized into subfolders based on each Pinterest board section. If disabled, all images are saved directly to the main folder.

## How it Works

- The script first logs into Pinterest using the provided credentials.
- It navigates to the specified board URL.
- The script downloads images from every subfolder it encounters up to one level deep. It does not recursively download from deeper folder levels.
- After downloading images from the subfolders, it returns to the main page and continues with the remaining images.

## Usage

To run the script, execute the following command in your terminal:

- python pinterest_downloader.py
