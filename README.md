# AI Discipline Code-Along: Ollama RAG
27 Mar 2024

This code-along will focus on a simple RAG implementation that runs locally on your machine using [Ollama](https://ollama.com/). In addition to installing the dependencies below, you'll want to have ready a PDF document with text content, on any topic. An HTML, Markdown, or plain text document works too.

## Dependencies

* Python 3.11+ (Rye will automatically use 3.11 by default; see below)
* VS Code (<https://code.visualstudio.com/>) with the Python extension (search in Extensions in the side bar)
* Rye (<https://rye-up.com/>), to manage the project’s Python third-party dependencies and Python interpreter version. For Windows users, you’ll likely want to use the 64-bit installer.
* Ollama (<https://ollama.com/>)

## Setup
First, clone this repo, and open the `ollama-rag.code-workspace` file in VS Code.

From the terminal in VS Code, install the Python dependencies using Rye:

```shell
$ rye sync
```

This will install the following Python dependencies in a virtual environment: `gradio ollama haystack-ai ollama-haystack pypdf`. If VS Code prompts you to select the new environment for the workspace, say yes.

Next, use Ollama to pull down the models you want to use. Do these two, at least:

```shell
$ ollama pull llama2
$ ollama pull nomic-embed-text
```

Test it out by chatting with it on the command line: 

```shell
$ ollama run llama2
```

If you’d like, check out the supported models at <https://ollama.com/library> and pull any that you’d like to try. Unless you have a powerful GPU, it’s recommended that you use models in the 7b-parameter and under category. If your machine only supports running on CPU and you want to speed that up, there are smaller models such as `gemma:2b` that you can try, although the performance will not be as good. In general, the more parameters the model has, the better its accuracy, the more resources it requires, and the more slowly it runs. I’ll be doing the code-along with the `llama2:7b` model, but feel free to experiment and use what you like best!
