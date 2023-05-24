#!/usr/local/bin/python3

import sys
import argparse
import logging.config

from db.ingest import db_ingest

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def main(args=None):

    if args is None:
        print("main2")
        args = sys.argv[1:]

    # while True:
    parsed_args = parse_args(args)
    if 'prompt' in parsed_args and parsed_args.prompt:
        do_prompt(parsed_args)

    elif 'ask' in parsed_args and parsed_args.ask:
        do_ask(parsed_args)
    
    elif 'db' in parsed_args and parsed_args.db:
        do_db(parsed_args)


def do_prompt(args):
    logger.info(f'Prompt: {args}')


def do_ask(args):
    logger.info(f'Ask: {args}')


def do_db(args):
    if 'ingest' in args and args.ingest:
        db_ingest(args.ingest)
    else:
        logger.error(f'No source content provided in arguments: {args}')


def parse_args(args):
    top_parser = argparse.ArgumentParser(description='Ask Godínez!')

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

    db_parser = sub_parser.add_parser('db',
                                      description='Manage content in DB that will be used as reference.')
    db_parser.add_argument('-i', '--ingest',
                           action='append',
                           help='Ingest new content to DB.')
    db_parser.add_argument('-c', '--clear',
                           action='store_true',
                           help='Clear DB from references (this will delete all content ingested).')
    db_parser.set_defaults(db=True)

    return top_parser.parse_args(args)


if __name__ == '__main__':
    main()
