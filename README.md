# rednote_pure

An example of generating a fashion portrait with OpenAI's GPT Image 2.

## Generate an image

1. Copy `.env.example` to `.env` and add your OpenAI API key. Keep `.env` private; it is ignored by Git.
2. Run `python3 generate_image.py` (Python 3 is required; no additional packages are needed).

The script requests an image from the OpenAI API and saves it as `assets/fashion_portrait.png`.
The sample image in this repository was created with ChatGPT's image-generation tool.
