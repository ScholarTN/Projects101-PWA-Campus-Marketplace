import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ItemCard from '../components/ItemCard';
import HousingCard from '../components/HousingCard';
import { searchItems, searchHousing } from '../services/api';

function SearchResults() {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get('q');
  const [items, setItems] = useState([]);
  const [housing, setHousing] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const [itemsData, housingData] = await Promise.all([
          searchItems(query),
          searchHousing(query)
        ]);
        setItems(itemsData);
        setHousing(housingData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching search results:', error);
        setLoading(false);
      }
    };
    
    if (query) {
      fetchResults();
    }
  }, [query]);

  if (loading) return <div className="loading">Searching...</div>;

  return (
    <div className="search-results">
      <h1>Search Results for "{query}"</h1>
      
      {items.length > 0 && (
        <section>
          <h2>Items for Sale</h2>
          <div className="items-grid">
            {items.map(item => (
              <ItemCard key={item.id} item={item} />
            ))}
          </div>
        </section>
      )}
      
      {housing.length > 0 && (
        <section>
          <h2>Housing Listings</h2>
          <div className="listings-grid">
            {housing.map(listing => (
              <HousingCard key={listing.id} listing={listing} />
            ))}
          </div>
        </section>
      )}
      
      {items.length === 0 && housing.length === 0 && (
        <p>No results found for your search.</p>
      )}
    </div>
  );
}

export default SearchResults;