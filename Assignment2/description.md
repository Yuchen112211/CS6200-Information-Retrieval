# Description of Assignment2
## The design of ranking function

### The model I am using here is simple vector space model, since we should not know any relevant files in advance. The progress of indexing and tokenization are covered in Assignment1, and the tokens will be used in this part of assignment.

### Ranking function's steps are explained as follows:

1. Load all the cfc file data into the ranking class object that I creates, tokenize them all.
2. Parse the query into terms, tokenize the query.
3. Compute the corresbonding term frequency(tf) and idf(inverse document frequency) of files and query, store them.
4. Get the cosine similarity of each document with the query, store them as scores.
5. Sort the scores by decreasing order, return sorted scores as result.

Previously I wonder if whether I should jump through the documents that contains only 1 query term, but that would somehow decrease the precision. So I decided to give reward on how many query terms that the document has, each additional term would be given some scores, so that the more distinct terms a document has, the more valuable it will be.

## How to Compile and Run

1. Open the repo.
2. To compute the overall result and see the image, run in terminal:
```bash
$ python testCFCQueries.py
```

For this step you'll need python's matplotlib package, if not installed, please install in terminal:
```bash
$ pip install matplotlib
```

Then you'll see the image, and just in case you close it by mistake, the image will be saved as "rst.png" in the repo.

The overall Averaged precision will be printed out in the terminal.

3. To run the web page for query searching, run in terminal:

```bash
$ python rankServer.py
```

Then open your browser, type in localhost:8000, you can see the web search page.
