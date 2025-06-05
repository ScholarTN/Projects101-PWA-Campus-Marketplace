import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { validateEmail, validatePassword } from '../utils/validators';

function AuthModal({ mode = 'login', onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [userType, setUserType] = useState('student');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signup, login } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    if (!validateEmail(email)) {
      return setError('Please enter a valid email address');
    }

    if (!validatePassword(password)) {
      return setError('Password must be at least 6 characters');
    }

    try {
      setLoading(true);
      if (mode === 'signup') {
        await signup(email, password, { name, userType });
      } else {
        await login(email, password);
      }
      onClose();
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  }

  return (
    <div className="auth-modal">
      <div className="auth-content">
        <button className="close-btn" onClick={onClose}>&times;</button>
        <h2>{mode === 'login' ? 'Login' : 'Sign Up'}</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          {mode === 'signup' && (
            <>
              <label>
                Name:
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </label>
              <label>
                I am a:
                <select
                  value={userType}
                  onChange={(e) => setUserType(e.target.value)}
                >
                  <option value="student">Student</option>
                  <option value="landlord">Landlord</option>
                </select>
              </label>
            </>
          )}
          <label>
            Email:
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Sign Up'}
          </button>
        </form>
        {mode === 'login' && (
          <p className="switch-mode">
            Don't have an account? <button onClick={() => onClose('signup')}>Sign up</button>
          </p>
        )}
        {mode === 'signup' && (
          <p className="switch-mode">
            Already have an account? <button onClick={() => onClose('login')}>Login</button>
          </p>
        )}
      </div>
    </div>
  );
}

export default AuthModal;