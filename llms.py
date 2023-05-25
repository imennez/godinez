
import os
import logging.config
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All, LlamaCpp

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('llms')

load_dotenv()
model_path_gpt4all = os.environ.get('MODEL_PATH_GPT4ALL')
model_path_llamacpp = os.environ.get('MODEL_PATH_LLAMACPP')

callbacks = [StreamingStdOutCallbackHandler()]
n_ctx = 1000

def get_llm_wrapper(name):
    match name:
        case 'GPT4All':
            return GPT4All(model=model_path_gpt4all, n_ctx=n_ctx, backend='gptj', callbacks=callbacks, verbose=False)
        case 'LlamaCpp':
            return LlamaCpp(model_path=model_path_llamacpp, n_ctx=n_ctx, callbacks=callbacks, verbose=False)
        case _default:
            raise Exception(f'Model {name} not supported!')
