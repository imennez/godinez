#!/usr/local/bin/python3

import os
import sys
import argparse
import logging.config
from dotenv import load_dotenv
from langchain.chains import RetrievalQA

from references import refs_ingest, refs_clear, refs_get_retreiver
from llms import get_llm_wrapper

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('irwin')

load_dotenv()

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parsed_args = parse_args(args)
    if 'refs' in parsed_args and parsed_args.refs:
        do_refs(parsed_args)

    elif 'ask' in parsed_args and parsed_args.ask:
        do_ask(parsed_args.ask, parsed_args.llm)
    

def do_ask(ask, llm_name):
    llm_name = llm_name if llm_name else 'GPT4All'
    logger.info(f'Using {llm_name} Model')
    return_source_documents = True

    retriever = refs_get_retreiver()
    llm = get_llm_wrapper(llm_name)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=return_source_documents)
    
    print(f'\n\nAsking Irwin: {ask}...')
    res = qa(ask)
    refs = res['source_documents']
    for document in refs:
        print(f'\n\n>> {document.metadata["source"]}: \n{document.page_content}')


def do_refs(args):
    logger.info(f'Refs: {args}')
    print(f'Refs: {args}')
    if 'ingest' in args and args.ingest:
        refs_ingest(args.ingest)
    elif 'clear' in args and args.clear:
        refs_clear()
    else:
        logger.error(f'Invalid argument found in: {args}')


def parse_args(args):
    top_parser = argparse.ArgumentParser(description='Ask Irwin!')

    top_parser.add_argument('-a', '--ask',
                            action='store',
                            help='Provide the question you want answered.')

    top_parser.add_argument('--llm',
                            action='store',
                            help='Specify the name of the LLM to use. Options: GPT4All or LlamaCpp')

    sub_parser = top_parser.add_subparsers()

    refs_parser = sub_parser.add_parser('refs',
                                        description='Manage DB of references.')
    refs_parser.add_argument('-i', '--ingest',
                             action='append',
                             help='Ingest new references to DB.')
    refs_parser.add_argument('-c', '--clear',
                             action='store_true',
                             help='Clear DB from references (this will delete all content ingested).')
    refs_parser.set_defaults(refs=True)

    return top_parser.parse_args(args)


if __name__ == '__main__':
    main()
