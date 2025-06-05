import { firestore, auth } from './firebase';
import { 
  collection, 
  query, 
  where, 
  getDocs, 
  addDoc, 
  doc, 
  getDoc, 
  updateDoc,
  arrayUnion,
  serverTimestamp 
} from 'firebase/firestore';

const API = {
  // Items
  getItems: async () => {
    const q = query(collection(firestore, 'items'), where('status', '==', 'active'));
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  },

  getItem: async (id) => {
    const docRef = doc(firestore, 'items', id);
    const docSnap = await getDoc(docRef);
    return docSnap.exists() ? { id: docSnap.id, ...docSnap.data() } : null;
  },

  createItem: async (itemData) => {
    const user = auth.currentUser;
    if (!user) throw new Error('Not authenticated');
    
    const newItem = {
      ...itemData,
      sellerId: user.uid,
      createdAt: serverTimestamp(),
      status: 'active',
      views: 0
    };
    
    const docRef = await addDoc(collection(firestore, 'items'), newItem);
    return docRef.id;
  },

  // Housing
  getHousingListings: async (filter = 'all') => {
    let q;
    if (filter === 'all') {
      q = query(collection(firestore, 'housing'), where('status', '==', 'available'));
    } else {
      q = query(
        collection(firestore, 'housing'),
        where('type', '==', filter),
        where('status', '==', 'available')
      );
    }
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  },

  createHousingListing: async (listingData) => {
    const user = auth.currentUser;
    if (!user) throw new Error('Not authenticated');
    
    const newListing = {
      ...listingData,
      landlordId: user.uid,
      postedAt: serverTimestamp(),
      status: 'available'
    };
    
    const docRef = await addDoc(collection(firestore, 'housing'), newListing);
    return docRef.id;
  },

  // Search
  searchItems: async (queryText) => {
    const q = query(
      collection(firestore, 'items'),
      where('keywords', 'array-contains', queryText.toLowerCase()),
      where('status', '==', 'active')
    );
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  },

  searchHousing: async (queryText) => {
    const q = query(
      collection(firestore, 'housing'),
      where('keywords', 'array-contains', queryText.toLowerCase()),
      where('status', '==', 'available')
    );
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  },

  // Messages
  sendMessage: async (conversationId, messageData) => {
    const user = auth.currentUser;
    if (!user) throw new Error('Not authenticated');
    
    const message = {
      ...messageData,
      senderId: user.uid,
      sentAt: serverTimestamp(),
      read: false
    };
    
    if (conversationId) {
      const convoRef = doc(firestore, 'conversations', conversationId);
      await updateDoc(convoRef, {
        messages: arrayUnion(message),
        updatedAt: serverTimestamp()
      });
    } else {
      const newConvo = {
        participants: [user.uid, messageData.recipientId],
        messages: [message],
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp()
      };
      const docRef = await addDoc(collection(firestore, 'conversations'), newConvo);
      return docRef.id;
    }
  }
};

export default API;