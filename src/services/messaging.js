import { messaging } from './firebase';
import { getToken, onMessage } from 'firebase/messaging';
import { firestore } from './firebase';
import { doc, setDoc } from 'firebase/firestore';

const VAPID_KEY = 'YOUR_VAPID_KEY_HERE';

// Request permission and get token
export const requestForToken = async (userId) => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      const token = await getToken(messaging, { vapidKey: VAPID_KEY });
      if (token) {
        // Save token to Firestore
        await setDoc(doc(firestore, 'fcmTokens', userId), {
          token,
          userId,
          createdAt: new Date()
        });
        return token;
      }
    }
  } catch (error) {
    console.error('Error getting FCM token:', error);
  }
};

// Listen for foreground messages
export const onMessageListener = () =>
  new Promise((resolve) => {
    onMessage(messaging, (payload) => {
      resolve(payload);
    });
  });

// Subscribe to topic (for housing alerts, etc.)
export const subscribeToTopic = async (token, topic) => {
  try {
    const response = await fetch('https://iid.googleapis.com/iid/v1/' + token + '/rel/topics/' + topic, {
      method: 'POST',
      headers: new Headers({
        'Authorization': 'key=YOUR_SERVER_KEY'
      })
    });
    return await response.json();
  } catch (error) {
    console.error('Error subscribing to topic:', error);
  }
};