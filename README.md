# Irwin

Why `Irwin`? Irwin is the kid who knew everything at school: https://youtu.be/CafPNEWnDhk?t=115

# Setup

## LLMs
First, you need to get the opensource LLMs supported by Irwin:

1. **GPT4All**: Easy, just download [here](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin).
1. **Llama.cpp**: This is a bit morew complicated.
    1. Clone [llama-dl](https://github.com/shawwn/llama-dl) project
    1. Modify variable `MODEL_SIZE` in `llama.sh` to only include `7B` (otherwise it will take too long and you will need too much disk space)
    1. Run `llama.sh`
    1. Clone [Llama.cpp](https://github.com/ggerganov/llama.cpp) project
    1. Follow steps in section [Prepare Data & Run](https://github.com/ggerganov/llama.cpp#prepare-data--run) of README.
1. Make models available to Irwin project. Suggestion, create folder `models` in project's root and move there.

## Environment

Copy `example.env` to `.env` file and adjust values:
- DB_DIR: Where to store reference embeddings
- MODEL_PATH_GPT4ALL: Where you have GPT4All model
- MODEL_PATH_LLAMACPP: Where you have Llama.cpp model

# Ingest References

To ingest content to be used as reference, first get the content you what to use in the format of `csv`, `html`, `pdf`, and `txt`. We support more, but keeping it simple for now.

**Options:**
- Appian Docs: Download Appian docs using `wget`, i.e.: `wget -r --no-parent https://docs.appian.com/suite/help/23.1/ `

Once you have your content, and accessible to `Irwin`, then run this command from `Irwin`'s replacing the relative path where you have your references:

`./irwin.py refs -i data/references`

# Ask a question

Now that you have the models ready and some reference documention, you can ask `Irwin` a question.

**Examples:**

By default, `Irwin` will use `GPT4All` model (faster performance)

`./irwin.py -a "Does Appian provide RPA?"`

If you want to explicitly use Llama.cpp, then pass flag `--llm` with the supported name:

`./irwin.py -a "Does Appian provide RPA?" --llm LlamaCpp`

