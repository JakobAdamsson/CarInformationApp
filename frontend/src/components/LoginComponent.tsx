import '../styles/LoginComponent.css'; // Import the CSS file
import React, { useState } from 'react';
const PREFIX: string = "login";

const LoginComponent: React.FC<{}> = ({ }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUserName] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'login' | 'signup' | ''>(''); // Track modal type
  

  const loginUser = (e: React.FormEvent) => {
    e.preventDefault();
    fetch(`http://localhost:5000/${PREFIX}/login_user`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
      .then(response => response.json())
      .then((data) => {
        alert(data.message);
        // Add further login success handling here
      })
      .catch(error => console.error('Error:', error));
  };

  const signUpUser = (e: React.FormEvent) => {
    e.preventDefault();
    fetch(`http://localhost:5000/${PREFIX}/sign_up_user`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, username }),
    })
      .then(response => response.json())
      .then((data) => {
        alert(data.message);
        // Add further signup success handling here
      })
      .catch(error => console.error('Error:', error));
  };

  const closeModal = () => {
    setShowModal(false);
    setModalType('');
  };

  const openLoginModal = () => {
    setModalType('login');
    setShowModal(true);
  };

  const openSignupModal = () => {
    setModalType('signup');
    setShowModal(true);
  };

  return (
    <div className="app-container">
      <div className="toggle-buttons">
        <button className="toggle-button" onClick={openLoginModal}>Logga in</button>
        <button className="toggle-button" onClick={openSignupModal}>Gå med</button>
      </div>

      {/* Modal for Login and Sign Up */}
      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{modalType === 'login' ? 'Login' : 'Sign Up'}</h2>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>

            <div className="modal-body">
              {modalType === 'login' ? (
                <form onSubmit={loginUser}>
                  <input
                    type="email"
                    value={email}
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <input
                    type="password"
                    value={password}
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <button type="submit" className="submit-button">Logga in</button>
                </form>
              ) : (
                <form onSubmit={signUpUser}>
                  <input
                    type="email"
                    value={email}
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <input
                    type="password"
                    value={password}
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <input
                    type="text"
                    value={username}
                    placeholder="Username"
                    onChange={(e) => setUserName(e.target.value)}
                    required
                  />
                  <button type="submit" className="submit-button">Gå med</button>
                </form>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LoginComponent;