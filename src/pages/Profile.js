import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { firestore } from '../services/firebase';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { useHistory } from 'react-router-dom';

function Profile() {
  const { currentUser, logout, updateEmail, updatePassword } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const history = useHistory();

  useEffect(() => {
    const fetchProfile = async () => {
      if (!currentUser) return;
      
      try {
        const userDoc = await getDoc(doc(firestore, 'users', currentUser.uid));
        if (userDoc.exists()) {
          setProfile(userDoc.data());
          setFormData(userDoc.data());
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching profile:', error);
        setLoading(false);
      }
    };
    
    fetchProfile();
  }, [currentUser]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    try {
      // Update email if changed
      if (formData.email !== currentUser.email) {
        await updateEmail(formData.email);
      }
      
      // Update profile in Firestore
      await updateDoc(doc(firestore, 'users', currentUser.uid), formData);
      
      setMessage('Profile updated successfully!');
      setEditMode(false);
      // Refresh to update currentUser in context
      history.go(0);
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) return <div className="loading">Loading profile...</div>;
  if (!profile) return <div>No profile data found</div>;

  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      
      {!editMode ? (
        <div className="profile-view">
          <div className="profile-header">
            <h2>{profile.name}</h2>
            <p>{profile.userType === 'landlord' ? 'Landlord' : 'Student'}</p>
          </div>
          
          <div className="profile-details">
            <p><strong>Email:</strong> {currentUser.email}</p>
            {profile.phone && <p><strong>Phone:</strong> {profile.phone}</p>}
            {profile.bio && <p><strong>Bio:</strong> {profile.bio}</p>}
            
            {profile.userType === 'student' && (
              <>
                <p><strong>University:</strong> {profile.university || 'Not specified'}</p>
                <p><strong>Major:</strong> {profile.major || 'Not specified'}</p>
              </>
            )}
            
            {profile.userType === 'landlord' && (
              <>
                <p><strong>Company:</strong> {profile.company || 'Not specified'}</p>
                <p><strong>Properties Listed:</strong> {profile.propertiesCount || 0}</p>
              </>
            )}
          </div>
          
          <div className="profile-actions">
            <button onClick={() => setEditMode(true)}>Edit Profile</button>
            <button onClick={logout}>Logout</button>
          </div>
        </div>
      ) : (
        <form className="profile-form" onSubmit={handleSubmit}>
          {error && <div className="error">{error}</div>}
          {message && <div className="message">{message}</div>}
          
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name || ''}
              onChange={handleChange}
              required
            />
          </label>
          
          <label>
            Email:
            <input
              type="email"
              name="email"
              value={formData.email || ''}
              onChange={handleChange}
              required
            />
          </label>
          
          <label>
            Phone:
            <input
              type="tel"
              name="phone"
              value={formData.phone || ''}
              onChange={handleChange}
            />
          </label>
          
          <label>
            Bio:
            <textarea
              name="bio"
              value={formData.bio || ''}
              onChange={handleChange}
            />
          </label>
          
          {profile.userType === 'student' && (
            <>
              <label>
                University:
                <input
                  type="text"
                  name="university"
                  value={formData.university || ''}
                  onChange={handleChange}
                />
              </label>
              
              <label>
                Major:
                <input
                  type="text"
                  name="major"
                  value={formData.major || ''}
                  onChange={handleChange}
                />
              </label>
            </>
          )}
          
          {profile.userType === 'landlord' && (
            <>
              <label>
                Company:
                <input
                  type="text"
                  name="company"
                  value={formData.company || ''}
                  onChange={handleChange}
                />
              </label>
              
              <label>
                License Number:
                <input
                  type="text"
                  name="licenseNumber"
                  value={formData.licenseNumber || ''}
                  onChange={handleChange}
                />
              </label>
            </>
          )}
          
          <div className="form-actions">
            <button type="submit">Save Changes</button>
            <button type="button" onClick={() => setEditMode(false)}>
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default Profile;