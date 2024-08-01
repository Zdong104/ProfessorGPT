# Professor Matching Tool

This repository provides a tool to help you select a suitable professor for your PhD program using a large language model (LLM). By inputting keywords or descriptions about the professor you're looking for, the Python code determines which professor from the CS ranking AI domain best matches your needs.

## Overview

The tool leverages a RAG (Retrieval-Augmented Generation) approach to compare and match your preferences with professors. The repository includes scripts to help you gather and analyze professor data, focusing on artificial intelligence (AI) professors listed on [CSRankings]([https://csrankings.org/#/index?all&us](https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&us).

## Features

- **Professor Matching:** Input keywords or descriptions to find the best-matching professors.
- **Data Collection:** Scripts to gather and store information about AI professors.
- **Information Extraction:** Tools to extract and process professor data for analysis.

## File Structure

- **`content.py`**: Script to collect and store professor information.
- **`professorinfo.py`**: Script to include additional professors and their home pages.
- **`storage.py`**: Manages data storage.
- **`input.py`**: Handles user inputs and interactions.
- **`llamaindex.ipynb`**: Jupyter notebook for information extraction.
- **`university_faculty_XXX.json`**: Intermediate JSON files containing professor data.

## Setup Instructions

1. **API Key Configuration:** Replace the environment file with your OpenAI API key to access the LLM services.

2. **Prepare Data:** Decompress the `default_Vector_store.zip` file to save tokens from embedding pure text from the professor's home pages.

3. **Run Scripts:** Use the provided Python scripts and Jupyter notebook to collect, store, and analyze professor information.

## Usage

1. **Collect Professor Data:** Use `content.py` and `professorinfo.py` to gather and manage professor information.

2. **Extract Information:** Run the `llamaindex.ipynb` notebook to process and analyze the data.

3. **Match Professors:** Input your preferences and descriptions to find the best-matching professor based on the analyzed data.

## Contributions

Feel free to contribute by adding more professors, updating the data collection scripts, or improving the matching algorithm. Pull requests are welcome!

## License

Free use, no license. 


@misc{dong2024professor,
  author       = {Z. Dong},
  title        = {Professor Matching Tool},
  year         = {2024},
  howpublished = {\url{https://github.com/your-username/your-repository-name}},
  note         = {Accessed: [date accessed]}
}



Here's a BibTeX citation if you need:

```bibtex
@misc{dong2024professor,
  author       = {Z. Dong},
  title        = {Professor Matching Tool},
  year         = {2024},
  howpublished = {\url{https://github.com/your-username/your-repository-name}},
  note         = {Accessed: [date accessed]}
}
```
