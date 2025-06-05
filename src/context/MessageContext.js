import React, { createContext, useContext, useState, useEffect } from 'react';
import { firestore } from '../services/firebase';
import { collection, query, where, onSnapshot, addDoc, serverTimestamp } from 'firebase/firestore';
import { useAuth } from './AuthContext';

const MessageContext = createContext();

export function useMessages() {
  return useContext(MessageContext);
}

export function MessageProvider({ children }) {
  const { currentUser } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser) {
      setConversations([]);
      setLoading(false);
      return;
    }

    const q = query(
      collection(firestore, 'conversations'),
      where('participants', 'array-contains', currentUser.uid)
    );

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const convos = [];
      let unread = 0;
      
      snapshot.forEach(doc => {
        const data = doc.data();
        const lastMessage = data.messages?.[data.messages.length - 1];
        
        if (lastMessage && !lastMessage.read && lastMessage.sender !== currentUser.uid) {
          unread++;
        }
        
        convos.push({
          id: doc.id,
          ...data
        });
      });
      
      setConversations(convos);
      setUnreadCount(unread);
      setLoading(false);
    });

    return unsubscribe;
  }, [currentUser]);

  const sendMessage = async (conversationId, messageText, recipientId) => {
    try {
      const message = {
        text: messageText,
        sender: currentUser.uid,
        read: false,
        timestamp: serverTimestamp()
      };

      if (conversationId) {
        // Existing conversation
        const convoRef = doc(firestore, 'conversations', conversationId);
        await updateDoc(convoRef, {
          messages: arrayUnion(message),
          lastUpdated: serverTimestamp()
        });
      } else {
        // New conversation
        await addDoc(collection(firestore, 'conversations'), {
          participants: [currentUser.uid, recipientId],
          messages: [message],
          lastUpdated: serverTimestamp()
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  };

  const markAsRead = async (conversationId) => {
    try {
      const convoRef = doc(firestore, 'conversations', conversationId);
      const convo = conversations.find(c => c.id === conversationId);
      
      if (convo) {
        const unreadMessages = convo.messages.filter(
          m => !m.read && m.sender !== currentUser.uid
        );
        
        if (unreadMessages.length > 0) {
          const updates = unreadMessages.map(msg => ({
            ...msg,
            read: true
          }));
          
          await updateDoc(convoRef, {
            messages: updates
          });
        }
      }
    } catch (error) {
      console.error('Error marking messages as read:', error);
    }
  };

  const value = {
    conversations,
    unreadCount,
    loading,
    sendMessage,
    markAsRead
  };

  return (
    <MessageContext.Provider value={value}>
      {children}
    </MessageContext.Provider>
  );
}