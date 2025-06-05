import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { firestore } from '../services/firebase';
import { collection, query, where, onSnapshot } from 'firebase/firestore';
import { requestForToken, onMessageListener } from '../services/messaging';

function NotificationBell() {
  const { currentUser } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    if (!currentUser) return;

    // Request notification permission and get FCM token
    requestForToken(currentUser.uid);

    // Set up listener for foreground messages
    const unsubscribeMessage = onMessageListener()
      .then((payload) => {
        const newNotification = {
          id: Date.now(),
          title: payload.notification.title,
          body: payload.notification.body,
          read: false,
          timestamp: new Date()
        };
        setNotifications(prev => [newNotification, ...prev]);
        setUnreadCount(prev => prev + 1);
      })
      .catch((err) => console.log('Failed: ', err));

    // Load stored notifications from Firestore
    const q = query(
      collection(firestore, 'notifications'),
      where('userId', '==', currentUser.uid),
      where('read', '==', false)
    );

    const unsubscribeSnapshot = onSnapshot(q, (snapshot) => {
      const newNotifications = [];
      snapshot.forEach(doc => {
        newNotifications.push({
          id: doc.id,
          ...doc.data()
        });
      });
      setNotifications(newNotifications);
      setUnreadCount(newNotifications.length);
    });

    return () => {
      unsubscribeMessage();
      unsubscribeSnapshot();
    };
  }, [currentUser]);

  const markAsRead = (id) => {
    if (id) {
      // Mark single notification as read
      setNotifications(prev =>
        prev.map(n => (n.id === id ? { ...n, read: true } : n))
      );
      setUnreadCount(prev => prev - 1);
      // Update in Firestore
      // (implementation depends on your backend)
    } else {
      // Mark all as read
      setNotifications(prev =>
        prev.map(n => ({ ...n, read: true }))
      );
      setUnreadCount(0);
      // Update all in Firestore
    }
  };

  return (
    <div className="notification-bell">
      <button onClick={() => setShowDropdown(!showDropdown)}>
        <i className="fas fa-bell"></i>
        {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
      </button>
      
      {showDropdown && (
        <div className="notification-dropdown">
          <div className="dropdown-header">
            <h4>Notifications</h4>
            <button onClick={() => markAsRead()}>Mark all as read</button>
          </div>
          
          {notifications.length === 0 ? (
            <p className="empty">No notifications</p>
          ) : (
            <ul>
              {notifications.map(notification => (
                <li 
                  key={notification.id} 
                  className={notification.read ? '' : 'unread'}
                  onClick={() => markAsRead(notification.id)}
                >
                  <strong>{notification.title}</strong>
                  <p>{notification.body}</p>
                  <small>
                    {new Date(notification.timestamp?.toDate()).toLocaleString()}
                  </small>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default NotificationBell;