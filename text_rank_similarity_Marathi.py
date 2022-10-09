import streamlit as st
from preprocess import cleanText
import networkx
import itertools
import math
import sys
import io
import json
import gradio as gr
sentenceDictionary = {}


def getSimilarity(sentenceID1, sentenceID2):
    commonWordCount = len(set(sentenceDictionary[sentenceID1]) & set(
        sentenceDictionary[sentenceID2]))
    denominator = math.log(len(
        sentenceDictionary[sentenceID1])) + math.log(len(sentenceDictionary[sentenceID2]))
    return commonWordCount/denominator if denominator else 0


def generateGraph(nodeList):
    graph = networkx.Graph()
    graph.add_nodes_from(nodeList)
    edgeList = list(itertools.product(nodeList, repeat=2))
    for edge in edgeList:
        graph.add_edge(edge[0], edge[1],
                       weight=getSimilarity(edge[0], edge[1]))
    return graph


def printDictionary():
    for key, val in sentenceDictionary.iteritems():
        print(str(key) + " : " + " ".join(sentenceDictionary[key]))


def textRankSimilarity(filePath):
    global sentenceDictionary
    summarySentenceCount = 5
    sentenceDictionary = {}
    sentences = []
    sentenceDictionary, sentences, size = cleanText(filePath)
    # printDictionary()
    graph = generateGraph(list(sentenceDictionary.keys()))
    # return(graph)
    pageRank = networkx.pagerank(graph)
    output = "\n".join([sentences[sentenceID] for sentenceID in sorted(
        sorted(pageRank, key=pageRank.get, reverse=True)[:summarySentenceCount])])
    return (output)


if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center;'>Text Summarization</h1>",
                unsafe_allow_html=True)
    uploaded_files = st.file_uploader('Upload text file', type=[
                                      'txt'], accept_multiple_files=False)
    if uploaded_files is not None:
        bytes_data = uploaded_files.read().decode('utf-8')
        result = textRankSimilarity(bytes_data)
        st.subheader("Input Text\n")
        st.markdown(f"<div style='text-align: justify;'>{bytes_data}</div>",
                    unsafe_allow_html=True)
        st.subheader("Summarized text\n")
        st.markdown(
            f"<div style='text-align: justify;'>{result}</div>",
            unsafe_allow_html=True)
    # textRankSimilarity(sys.argv[1])
