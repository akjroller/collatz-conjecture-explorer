# Collatz Conjecture Explorer

This repository contains an API and a computation service for exploring and understanding the Collatz Conjecture, an unsolved problem in mathematics.

## Features

The Collatz Conjecture Explorer offers several features:

- Continual calculation of Collatz sequences starting from any given number, and storage of these results in a SQLite database.
- A RESTful API for querying the results of these calculations, including specific sequences, statistical summaries, and more.
- Ability to query Collatz sequences for a specific range of numbers or search sequences by specific criteria.
- Ability to retrieve the top N sequences with the highest number of steps, as well as average statistics over a specified number of sequences.
- The computation service automatically updates distribution statistics when it's shut down.

## Requirements

- Python 3.11 or newer
- SQLite3
- FastAPI
- Uvicorn (for serving the API)

## Docker Installation

To run the Collatz Conjecture Explorer using Docker, follow these steps:

1. Clone this repository using git:

   ```bash
   git clone https://github.com/akjroller/collatz_conjecture_explorer.git
   cd collatz_conjecture_explorer
   ```

2. Build and start the Docker containers:

   ```bash
   docker compose up --build -d
   ```

   This command will build the Docker images and start the services in the background.

3. Access the API:

   The API will be accessible at http://localhost:8001. For example, to get the Collatz sequence for the number 6, you would access http://localhost:8001/collatz/6.

## Manual Installation

First, clone this repository using git:

```bash
git clone https://github.com/akjroller/collatz_conjecture_explorer.git
cd collatz_conjecture_explorer
```

Then install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

change admin password in config.py

To start the computation service, run:

```bash
python collatz.py
```

The computation service will continually calculate Collatz sequences and store the results in a SQLite database.

To start the API, run:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

You can then access the API at http://localhost:8000. For example, to get the Collatz sequence for the number 6, you would access http://localhost:8000/collatz/6.

## Public Access

The API is publicly accessible at `https://collatz.therollermethod.com`. For example, to get the Collatz sequence for the number 6, you can access it at: https://collatz.therollermethod.com/collatz/6.

## API Endpoints

Here are some of the API endpoints you can use:

- /collatz/{num}: Get the Collatz sequence and its statistics for a specific starting number.
- /stats: Get the overall computation statistics, including the last checked number, total computation time, and average steps.
- /collatz/range/{start}/{end}: Get the Collatz sequences for a range of starting numbers.
- /collatz/top/{n}: Get the top N Collatz sequences with the highest number of steps.
- /collatz/average/{n}: Get the average number of steps and average max value over the last N Collatz sequences.
- /collatz/search/{number_of_steps}/{max_value}: Search for Collatz sequences by a specific number of steps and max value.
- /collatz/stats/hourly: Get the hourly Collatz computation statistics.
- /collatz/stats/distribution: Get the distribution statistics for Collatz computations. (Not yet implemented)

## Notes

The computation service can be interrupted with CTRL+C or by closing your CLI , at which point it will calculate and store distribution statistics.

The API includes a middleware for blocking requests from specific IPs. The list of blocked IPs can be updated by adding them to blocked_ips.txt and using the /refresh_block_list/{password} endpoint with the correct password.

## Contributing

Contributions are welcome! Please create an issue to discuss the changes or open a pull request.

## License

This project is licensed under the terms of the MIT license.

## Contact

If you have any questions, you can contact the author at awakengaming83@gmail.com.
