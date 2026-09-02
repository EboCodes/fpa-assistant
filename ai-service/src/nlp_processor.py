# ai-service/src/nlp_processor.py
"""
NLP Processing module
Handles text preprocessing, tokenization, and embedding generation
"""

import nltk
import os
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from sentence_transformers import SentenceTransformer, util
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    """Handle NLP preprocessing and embedding generation"""
    
    def __init__(self):
        """Initialize NLP components"""
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            logger.warning('NLTK stopwords data is unavailable; continuing without stopword filtering.')
            self.stop_words = set()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Load embedding model
        self.embedding_model = None
        self.embedding_model_name = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        self.embedding_model_load_attempted = False
        
        logger.info("✅ NLP Processor initialized")
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra spaces
        text = re.sub(r'[^a-zA-Z0-9\s\?\!]', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text):
        """Tokenize text into words"""
        try:
            return word_tokenize(text)
        except LookupError:
            return wordpunct_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from tokens"""
        filtered = [token for token in tokens if token not in self.stop_words]
        return filtered
    
    def lemmatize(self, tokens):
        """Lemmatize tokens"""
        try:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except LookupError:
            logger.warning('NLTK wordnet data is unavailable; continuing without lemmatization.')
            return tokens

    def _get_embedding_model(self):
        """Load the optional transformer model only when semantic search is used."""
        if self.embedding_model is None and not self.embedding_model_load_attempted:
            self.embedding_model_load_attempted = True
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
            except Exception as error:
                logger.warning('Embedding model could not be loaded (%s); using lexical fallback.', error)
                return None
        return self.embedding_model
    
    def process(self, text):
        """
        Process text through complete NLP pipeline
        Returns processed text
        """
        # Clean text
        cleaned = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        # Remove stopwords
        filtered = self.remove_stopwords(tokens)
        
        # Lemmatize
        lemmatized = self.lemmatize(filtered)
        
        # Return joined text
        processed_text = ' '.join(lemmatized)
        
        return processed_text
    
    def extract_entities(self, text):
        """
        Extract named entities from text using spaCy
        Returns list of entities
        """
        if not self.nlp:
            logger.warning("spaCy model not available for entity extraction")
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_
            })
        
        return entities
    
    def get_embeddings(self, texts):
        """
        Generate embeddings for texts using SentenceTransformer
        Returns list of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        model = self._get_embedding_model()
        if model is not None:
            embeddings = model.encode(texts, convert_to_tensor=False)
            return [emb.tolist() for emb in embeddings]

        # A deterministic fallback keeps the API available when model weights are
        # not installed (for example, during an offline first run).
        vectors = []
        for text in texts:
            vector = np.zeros(384, dtype=float)
            for token in self.process(text).split():
                vector[hash(token) % len(vector)] += 1
            vectors.append(vector.tolist())
        return vectors
    
    def calculate_cosine_similarity(self, embedding1, embedding2):
        """
        Calculate cosine similarity between two embeddings
        Returns similarity score (0-1)
        """
        # Convert to numpy arrays if they're lists
        if isinstance(embedding1, list):
            embedding1 = np.array(embedding1)
        if isinstance(embedding2, list):
            embedding2 = np.array(embedding2)
        
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        emb1_norm = embedding1 / norm1
        emb2_norm = embedding2 / norm2
        
        # Calculate cosine similarity
        similarity = np.dot(emb1_norm, emb2_norm)
        
        return float(similarity)
    
    def find_similar_texts(self, query, candidates, threshold=0.5):
        """
        Find similar texts to query from candidates
        Returns list of similar texts with scores
        """
        model = self._get_embedding_model()
        if model is None:
            query_embedding = self.get_embeddings([query])[0]
            results = []
            for candidate, embedding in zip(candidates, self.get_embeddings(candidates)):
                score = self.calculate_cosine_similarity(query_embedding, embedding)
                if score >= threshold:
                    results.append({'text': candidate, 'score': score})
            return sorted(results, key=lambda item: item['score'], reverse=True)
        query_embedding = model.encode(query)
        candidate_embeddings = model.encode(candidates)
        
        # Calculate similarities
        similarities = util.cos_sim(query_embedding, candidate_embeddings)[0]
        
        # Filter by threshold and sort
        results = []
        for idx, score in enumerate(similarities):
            if score >= threshold:
                results.append({
                    'text': candidates[idx],
                    'score': float(score)
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def get_keywords(self, text, top_n=5):
        """
        Extract top keywords from text
        Returns list of keywords
        """
        # Process text
        processed = self.process(text)
        tokens = processed.split()
        
        # Simple keyword extraction (can be improved with TF-IDF)
        # Return top N most common terms
        from collections import Counter
        freq = Counter(tokens)
        keywords = [word for word, _ in freq.most_common(top_n)]
        
        return keywords
