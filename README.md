
# GitBot

Follow these instructions to set up the development environment.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LetsTrie/gitbot.git
   cd gitbot
   ```

2. **Set up Poetry**:
   ```bash
   pip install poetry
   poetry config virtualenvs.in-project true
   poetry install
   ```

3. **Activate the environment**:
   ```bash
   poetry shell
   ```

## Running the Program

After setting up the environment, run the following command:

   ```bash
   sh run.sh
   ```

## Environment Variables

Create a `.env` file in the project root with the following:

```
OPENAI_API_KEY=<your-openai-api-key>
GITHUB_ACCESS_TOKEN=<your-github-access-token>
ENVIRONMENT=<dev/prod>
```