import React, { useEffect, useState } from 'react';

function App() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/listings")
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        const arr = Array.isArray(data) ? data : data.listings ?? [];
        setListings(arr);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);
  

  if (loading) return <div style={{ padding: 16 }}>Loading…</div>;
  if (error)   return <div style={{ padding: 16, color: 'red' }}>Error: {error}</div>;

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 16 }}>
      <h1>Job Listings</h1>
      {listings.length === 0 && <p>No listings found.</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {listings.map(l => (
          <li key={l.id} style={{ margin: '12px 0', padding: 12, border: '1px solid #ccc', borderRadius: 4 }}>
            <strong>{l.title}</strong><br/>
            {l.location} • {l.type}<br/>
            Exp: {l.experience} • Salary: {l.salary}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
