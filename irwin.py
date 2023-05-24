#!/usr/local/bin/python3

import sys
import argparse
import logging.config

from db.references import refs_ingest, refs_clear

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parsed_args = parse_args(args)
    logger.info(f'parsed_args: {parsed_args}')
    if 'prompt' in parsed_args and parsed_args.prompt:
        do_prompt(parsed_args)

    elif 'ask' in parsed_args and parsed_args.ask:
        do_ask(parsed_args)
    
    elif 'refs' in parsed_args and parsed_args.refs:
        do_refs(parsed_args)


def do_prompt(args):
    logger.info(f'Prompt: {args}')


def do_ask(args):
    logger.info(f'Ask: {args}')


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

    sub_parser = top_parser.add_subparsers()

    prompt_parser = sub_parser.add_parser('prompt',
                                          description='Manage prompts to provide context.')
    prompt_parser.set_defaults(prompt=True)
    prompt_parser.add_argument('-a', '--add',
                               action='store',
                               help='Add a prompt')
    prompt_parser.add_argument('-l', '--list',
                               action='store_true',
                               help='List queued prompts.')

    ask_parser = sub_parser.add_parser('ask',
                                       description='Ask question.')
    ask_parser.set_defaults(ask=True)

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
