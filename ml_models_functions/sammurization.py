import streamlit as st
from torch import nn


@st.cache(hash_funcs={nn.parameter.Parameter: lambda _: None})
def load_model():
    from transformers import PegasusTokenizer, PegasusForConditionalGeneration

    # Let's load the model and the tokenizer
    model_name = "human-centered-summarization/financial-summarization-pegasus"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer


@st.cache
def summarize(articles):
    model = load_model()[0]
    tokenizer = load_model()[1]
    summaries = []
    for article in articles:
        input_ids = tokenizer.encode(article, return_tensors="pt")
        output = model.generate(input_ids, max_length=55, num_beams=5, early_stopping=True)
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        summaries.append(summary)

    return summaries


@st.cache(allow_output_mutation=True)
def load_transformers():
    from transformers import pipeline
    sentiment = pipeline("sentiment-analysis")
    return sentiment
