# ReadProbe
**An AI-powered tool to support lateral reading.**

## About

Lateral reading is a critical thinking approach used to evaluate the 
credibility and accuracy of information found online by stepping away 
from the initial source and exploring other sources to verify its 
authenticity. Lateral reading can reduce the risk of being misled by 
misinformation, propaganda, and other forms of disinformation. 
By cross-referencing information with multiple sources, users can become 
more informed and responsible consumers of information, promoting a better 
online community.

Live demo: https://readprobe.streamlit.app/. This web interface is to 
illustrate how this tool works and collect early feedback from users. 
For future work, **ReadProbe** could be embedded into a browser extension 
where users can directly select the text they want to probe into in the 
same tab without the hassle to copy and paste the text into a new tab.

## Overview

The figure below shows how **ReadProbe** works, especially the data flow
among different components.

<p align="center">
   <img src="overview.png" alt="An overview figure of ReadProbe" title="ReadProbe Design Overview">
</p>

## Features

- **Question Generation**: To support lateral reading, we prompt OpenAI's 
[ChatGPT](https://openai.com/blog/chatgpt) to come up with **five**
questions that the user may ask when reading the input text.
- **Bing Search**: For each generated question, we call the
[Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)
to find relevant documents to answer the question. This module strengthens
ChatGPT's knowledge of events that happened after 2021 and mitigates its
known behavior to fabricate facts.
- **Relevance Ranking**: Web documents are usually long and only parts of
them are relevant to the question. Due to the input limit (4096 tokens) of
ChatGPT, we break the top **three** most relevant documents into text chunks 
(each with 256 words) and then select the most relevant **six** chunks to 
construct the input to the ChatGPT to generate the answer. To measure the
relevance, we use OpenAI's 
[text-embedding model](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)
to obtain semantic vectors for both the question and text chunks and then
select the top **six** most relevant chunks based on their cosine similarity
with the question.
- **Answer Generation**: With the question and relevant chunks from **Bing Search** 
module and **Relevance Ranking** module, we prompt ChatGPT
to answer the question by summarizing those relevant chunks.
- **Anonymous User Feedback**: We log two kinds of user actions for future improvements: 
content generation (collecting the user input and generated questions 
and answers) and thumbs-up (collecting the corresponding question and 
answer that the user likes). To make sure anonymity, we generated a random id
using `uuid.uuid4()` for each content generation. We use 
[Google Forms](https://docs.google.com/forms/) as a 
lightweight database to store our logs.
- **Input Moderation**: Several checks are performed to avoid undesired
user inputs. Specifically, we check the input length to make sure the user
input provides enough context for ChatGPT to generate meaningful questions
and does not exceed the input limit of ChatGPT (4096 tokens). We also check
the input language using [langdetect](https://github.com/Mimino666/langdetect), 
because we only support English for now. Finally, we call OpenAI's
[moderation endpoint](https://platform.openai.com/docs/guides/moderation/overview)
to prohibit malicious content, such as violence or hate.

*\* We use the phrase "content generation" to refer to the process of generating questions
and corresponding answers for a given user input.*

## Installation Instructions
### Run this project on a local machine

### Deploy on Streamlit


## Q&A
1. How to run this project on my local machine? \
Make sure you have [Streamlit](https://streamlit.io/) installed. 
Then run this command in the root repository of this project 
`streamlit run main.py`. 
   1. Bing API: free , how to get.


## Evaluation

To empirically evaluate the effectiveness of this web app in real-life scenarios,
we conducted a small-scale pilot user study by asking our friends to try using
this tool.
To mimic real use cases, we didn't provide additional context or explanations
other than those shown in the web app itself.
Here is our instruction for the pilot user study.
> We developed a tool to help users perform lateral reading 
> using OpenAI services. Thanks for agreeing to participate in
> this pilot user study. Some of your usage data will be collected 
> anonymously. Please spend at least 10 minutes playing with this web
> application: https://readprobe.streamlit.app/. 
> You are encouraged to click on the "I like this one" button to indicate
> that you like the generated question and answer, e.g., they are
> very relevant or helpful.
> You may choose to quit this study anytime.
> Once finished, please contact us to provide feedback on what aspects 
> you like or dislike this application. Thanks again for your valuable time.

X participants joined this pilot study. Here, we express our gratitude to
their valuable feedback. We summarized their feedback into several points
shown below:
- Positive
  1. asdas
- Negative
  1. Gneration is slow.

Note that our friends may be biased to giving positive feedback. 
A more formal and large-scale user study is required to demonstrate the 
usefulness of this tool.

s
## :warning: Disclaimer

Content generation in this web application is performed mainly by calling 
OpenAI APIs and Bing APIs. Even though we perform some postprocessing to 
improve the quality of generated content, due to our limited knowledge of 
the models behind those services, we can not make sure the generated 
content won't contain biased, unethical, incorrect, or controversial 
information. Please be aware of the potential risks of using this tool. 
**Contents generated in this web application don't represent the opinions of the
developers in this project.**
If you notice potentially malicious content generated by this app, 
please open an [issue](https://github.com/DakeZhang1998/ReadProbe/issues) 
to report. Your valuable feedback is deeply appreciated.

## License

This project is under the [GNU General Public License](LICENSE).

Deliverables

t the end of the hackathon, your team is asked to submit the following:

A live prototype solution, and
Hint: depending on the nature of your app, you may be able to deploy it for free at https://vercel.com/
An open-source program with installation instructions uploaded to GitHub and licensed under GNU GPLv3.
The source code should include a readme document that will (a) outline your solution, (b) describe all planned and implemented functionalities, (c) how your solution can be deployed to fight misinformation online and by whom and (d) whether and how you evaluated its effectiveness.
