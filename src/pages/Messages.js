import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useMessages } from '../context/MessageContext';
import { useAuth } from '../context/AuthContext';
import { firestore } from '../services/firebase';
import { doc, getDoc } from 'firebase/firestore';
import MessageList from '../components/MessageList';
import MessageForm from '../components/MessageForm';

function Messages() {
  const { conversations, unreadCount, loading, markAsRead } = useMessages();
  const { currentUser } = useAuth();
  const history = useHistory();
  const [selectedConvo, setSelectedConvo] = useState(null);
  const [otherUser, setOtherUser] = useState(null);

  useEffect(() => {
    if (conversations.length > 0 && !selectedConvo) {
      setSelectedConvo(conversations[0].id);
    }
  }, [conversations, selectedConvo]);

  useEffect(() => {
    const fetchOtherUser = async () => {
      if (!selectedConvo) return;
      
      const convo = conversations.find(c => c.id === selectedConvo);
      if (!convo) return;
      
      const otherUserId = convo.participants.find(id => id !== currentUser.uid);
      const userDoc = await getDoc(doc(firestore, 'users', otherUserId));
      
      if (userDoc.exists()) {
        setOtherUser(userDoc.data());
      }
      
      // Mark messages as read when conversation is selected
      markAsRead(selectedConvo);
    };
    
    fetchOtherUser();
  }, [selectedConvo, conversations, currentUser, markAsRead]);

  if (loading) return <div className="loading">Loading messages...</div>;

  return (
    <div className="messages-page">
      <div className="conversation-list">
        <h2>Conversations</h2>
        {conversations.length === 0 ? (
          <p>No conversations yet</p>
        ) : (
          <ul>
            {conversations.map(convo => {
              const otherUserId = convo.participants.find(id => id !== currentUser.uid);
              const lastMessage = convo.messages[convo.messages.length - 1];
              const isUnread = lastMessage && !lastMessage.read && lastMessage.sender !== currentUser.uid;
              
              return (
                <li
                  key={convo.id}
                  className={`convo-item ${selectedConvo === convo.id ? 'active' : ''} ${isUnread ? 'unread' : ''}`}
                  onClick={() => setSelectedConvo(convo.id)}
                >
                  <span className="other-user">{otherUserId}</span>
                  <span className="last-message">{lastMessage.text}</span>
                  <span className="time">
                    {new Date(lastMessage.timestamp?.toDate()).toLocaleTimeString()}
                  </span>
                </li>
              );
            })}
          </ul>
        )}
      </div>
      
      <div className="message-view">
        {selectedConvo ? (
          <>
            <div className="message-header">
              {otherUser && (
                <h3>
                  {otherUser.name}
                  {otherUser.userType === 'landlord' && ' (Landlord)'}
                </h3>
              )}
              <button onClick={() => history.push(`/profile/${otherUser?.uid}`)}>
                View Profile
              </button>
            </div>
            
            <MessageList conversationId={selectedConvo} />
            <MessageForm conversationId={selectedConvo} recipientId={otherUser?.uid} />
          </>
        ) : (
          <div className="no-convo-selected">
            <p>Select a conversation or start a new one</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Messages;