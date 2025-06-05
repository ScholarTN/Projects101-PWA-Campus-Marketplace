import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getMessaging } from "firebase/messaging";

// Your Firebase Config (use the one from your console)
const firebaseConfig = {
  apiKey: "AIzaSyDRwZH574pzS9CArAsZcuMhyGHn3-gTk8w",
  authDomain: "campus-marketplace-86db6.firebaseapp.com",
  projectId: "campus-marketplace-86db6",
  storageBucket: "campus-marketplace-86db6.appspot.com", // Fixed the bucket name
  messagingSenderId: "916950412760",
  appId: "1:916950412760:web:258cfa51610fa9748456ad",
  measurementId: "G-LF1GN19MKL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const messaging = getMessaging(app);

// (Optional) Analytics - only if you need it
// import { getAnalytics } from "firebase/analytics";
// export const analytics = getAnalytics(app);