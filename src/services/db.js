import { firestore } from './firebase';
import { 
  collection, 
  doc, 
  setDoc, 
  getDoc, 
  updateDoc,
  arrayUnion,
  arrayRemove,
  serverTimestamp
} from 'firebase/firestore';

const DB = {
  // User operations
  createUserProfile: async (userId, userData) => {
    const userRef = doc(firestore, 'users', userId);
    await setDoc(userRef, {
      ...userData,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp()
    });
    return true;
  },

  getUserProfile: async (userId) => {
    const userRef = doc(firestore, 'users', userId);
    const userSnap = await getDoc(userRef);
    return userSnap.exists() ? userSnap.data() : null;
  },

  updateUserProfile: async (userId, updates) => {
    const userRef = doc(firestore, 'users', userId);
    await updateDoc(userRef, {
      ...updates,
      updatedAt: serverTimestamp()
    });
    return true;
  },

  // Favorites
  addFavorite: async (userId, itemId, itemType) => {
    const userRef = doc(firestore, 'users', userId);
    await updateDoc(userRef, {
      favorites: arrayUnion({ id: itemId, type: itemType }),
      updatedAt: serverTimestamp()
    });
    return true;
  },

  removeFavorite: async (userId, itemId, itemType) => {
    const userRef = doc(firestore, 'users', userId);
    await updateDoc(userRef, {
      favorites: arrayRemove({ id: itemId, type: itemType }),
      updatedAt: serverTimestamp()
    });
    return true;
  },

  // Notifications
  createNotification: async (userId, notification) => {
    const notificationsRef = collection(firestore, 'notifications');
    await addDoc(notificationsRef, {
      ...notification,
      userId,
      read: false,
      createdAt: serverTimestamp()
    });
    return true;
  },

  markNotificationAsRead: async (notificationId) => {
    const notificationRef = doc(firestore, 'notifications', notificationId);
    await updateDoc(notificationRef, {
      read: true,
      readAt: serverTimestamp()
    });
    return true;
  }
};

export default DB;