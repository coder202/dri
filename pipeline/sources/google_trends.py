import logging
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from pipeline.utils.db import insert_signal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_trending_searches(pytrends):
    """Fetch daily trending searches using pytrends"""
    try:
        # Try different approaches for trending searches
        # Method 1: trending_searches (may be deprecated)
        trending_searches = pytrends.trending_searches(pn='united_states')
        if trending_searches is not None and not trending_searches.empty:
            logger.info("Using trending_searches method")
            return trending_searches[0].tolist()
        
        # Method 2: Use today_searches as fallback
        logger.info("trending_searches failed, trying today_searches")
        today_searches = pytrends.today_searches(pn='united_states')
        if today_searches is not None and not today_searches.empty:
            return today_searches[0].tolist()
        
        # Method 3: Use hardcoded trending topics as fallback
        logger.warning("Both API methods failed, using fallback keywords")
        fallback_keywords = [
            "artificial intelligence", "machine learning", "climate change", 
            "cryptocurrency", "electric vehicles", "remote work",
            "inflation", "supply chain", "cybersecurity", "renewable energy"
        ]
        return fallback_keywords
        
    except Exception as e:
        logger.error(f"Error fetching trending searches: {e}", exc_info=True)
        # Return fallback keywords
        logger.warning("Using fallback keywords due to API failure")
        fallback_keywords = [
            "artificial intelligence", "machine learning", "climate change", 
            "cryptocurrency", "electric vehicles", "remote work",
            "inflation", "supply chain", "cybersecurity", "renewable energy"
        ]
        return fallback_keywords

def get_interest_over_time(pytrends, keyword, timeframe='now 7-d'):
    """Get interest over time for a specific keyword"""
    try:
        pytrends.build_payload(kw_list=[keyword], timeframe=timeframe)
        df = pytrends.interest_over_time()
        
        if df.empty:
            return 0
            
        # Calculate average interest over the period
        return df[keyword].mean()
    except Exception as e:
        logger.error(f"Error getting interest over time for '{keyword}': {e}")
        return 0

def get_related_queries_count(pytrends, keyword):
    """Get count of related queries for a keyword"""
    try:
        pytrends.build_payload(kw_list=[keyword])
        related_queries = pytrends.related_queries()
        
        if not related_queries or keyword not in related_queries:
            return 0
            
        top_queries = related_queries[keyword]['top']
        rising_queries = related_queries[keyword]['rising']
        
        # Count unique related queries
        related_count = 0
        if top_queries is not None:
            related_count += len(top_queries)
        if rising_queries is not None:
            related_count += len(rising_queries)
            
        return related_count
    except Exception as e:
        logger.error(f"Error getting related queries for '{keyword}': {e}")
        return 0

def run():
    try:
        logger.info("Initializing Google Trends client...")
        # Initialize pytrends with proper parameters
        pytrends = TrendReq(
            hl='en-US',
            tz=360,  # UTC offset in minutes
            timeout=(10, 25),  # (connect, read) timeouts in seconds
            retries=1,  # Reduced retries to avoid rate limiting
            backoff_factor=0.5  # Increased backoff
        )
        
        logger.info("Fetching trending searches...")
        keywords = get_trending_searches(pytrends)
        
        if not keywords:
            logger.warning("No trending searches found")
            return
            
        logger.info(f"Found {len(keywords)} trending searches")
        
        for keyword in keywords:
            try:
                # Get interest over time (velocity)
                velocity = get_interest_over_time(pytrends, keyword)
                
                # Get related queries count (delta)
                related_count = get_related_queries_count(pytrends, keyword)
                delta = related_count / 10.0  # Normalize to a 0-10 scale
                
                # Calculate CSI (Consumer Sentiment Index)
                csi = (velocity * 0.7) + (delta * 0.3)
                
                # Log the data we're about to insert
                logger.info(f"Processing: {keyword} | Velocity: {velocity:.2f} | Related: {related_count} | CSI: {csi:.2f}")
                
                # Insert into database
                insert_signal(
                    datetime.utcnow(),
                    "google_trends",
                    keyword,
                    velocity,
                    delta,
                    csi,
                    "consumer"
                )
                
                # Be nice to Google's servers - increased delay
                import time
                time.sleep(7)
                
            except Exception as e:
                logger.error(f"Error processing keyword '{keyword}': {e}", exc_info=True)
                continue
                
    except Exception as e:
        logger.error(f"Unexpected error in Google Trends pipeline: {e}", exc_info=True)
    finally:
        logger.info("Google Trends pipeline completed")
