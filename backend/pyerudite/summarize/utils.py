"""Utility functions for the summarize app."""

import os

import openai
import spacy
import tiktoken
from django.conf import settings

from . import prompts


def count_tokens(text=None, model=None):
    """Count tokens in a text string using tiktoken."""
    model = settings.SUMMARY_MODEL
    encoding = model["encoding"]
    enc = tiktoken.get_encoding(encoding)
    tokens = enc.encode(text)
    token_count = len(tokens)
    return token_count


def split_text(text_path=None, title=None):
    """
    Split text into chunks of no more than max_tokens, using spaCy, so that
    full sentences are never broken up.

    :text_path: The path to the text file.
    :title: The title of the source. We need this here because it is part
      of our prompt and we need the full prompt in order to count the total
      tokens.

    :returns: A tuple of (chunks, total_token_count).

    """
    model = settings.SUMMARY_MODEL

    prompt_tokens = count_tokens(
        prompts.CONSISE_SUMMARY.format(chunk="", title=title)
    )
    max_tokens = model["max_tokens"] - prompt_tokens - model["response_tokens"]

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")

    with open(text_path, "r") as f:
        text = f.read()

    doc = nlp(
        text, disable=["tagger", "parser", "ner", "lemmatizer", "textcat"]
    )
    chunks = []
    current_chunk = []

    for sent in doc.sents:
        sent_text = sent.text.strip()  # this is one sentence
        sent_tokens = count_tokens(sent_text)

        if (
            sum([count_tokens(chunk) for chunk in current_chunk]) + sent_tokens
            > max_tokens
        ):
            # the sentence would make the chunk too big, so start a new chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent_text]
        else:
            # the sentence still fits into the current chunk
            current_chunk.append(sent_text)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    total_token_count = sum([count_tokens(chunk) for chunk in chunks])
    return chunks, total_token_count


def summarize_chunks(chunks=None, title=None):
    """
    Requests one summary per chunk and returns all OpenAI responses.

    :text: The text to be summarized.
    :summaries_path: The path to the summaries directory.

    """
    model = settings.SUMMARY_MODEL
    summaries = []
    for chunk in chunks:
        client = openai.Client(api_key=settings.OPENAI_API_KEY)
        prompt = prompts.CONSISE_SUMMARY.format(chunk=chunk, title=title)
        result = client.chat.completions.create(
            model=model["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=model["response_tokens"],
            temperature=0,
            n=1,
            stream=False,
        )
        summaries.append(result)
    return summaries


def save_summaries(
    summarize_obj=None, summaries=None, filename=None, summaries_path=None
):
    """
    Saves summaries to a text file, and returns the path to the file.

    Also calculates the total number of tokens used, and the cost of the
    API calls.

    :summarize_obj: The SummarizeFromIngest object.
    :summaries: A list of OpenAI responses.
    :filename: The filename of the source text file.
    :summaries_path: The path to the summaries directory.

    :returns: The updated SummarizeFromIngest object.

    """
    if summaries_path is None:
        summaries_path = os.path.join(
            settings.MEDIA_ROOT, "summarize/summaries"
        )

    if not os.path.exists(summaries_path):
        os.makedirs(summaries_path)

    model = settings.SUMMARY_MODEL

    total_input_tokens_used = 0
    total_output_tokens_used = 0
    summary_path = os.path.join(summaries_path, f"{filename}.txt")
    with open(summary_path, "w") as f:
        for summary in summaries:
            f.write(summary.choices[0].message.content)
            f.write("\n\n")
            total_input_tokens_used += summary.usage.prompt_tokens
            total_output_tokens_used += summary.usage.completion_tokens

    total_input_cost = (
        total_input_tokens_used * model["cost_per_1k_input_tokens_usd"] / 1000
    )
    total_output_cost = (
        total_output_tokens_used * model["cost_per_1k_output_tokens_usd"] / 1000
    )
    summarize_obj.input_tokens = total_input_tokens_used
    summarize_obj.output_tokens = total_output_tokens_used
    summarize_obj.input_cost = total_input_cost
    summarize_obj.output_cost = total_output_cost
    summarize_obj.status = "completed"
    summarize_obj.save()

    return summarize_obj
